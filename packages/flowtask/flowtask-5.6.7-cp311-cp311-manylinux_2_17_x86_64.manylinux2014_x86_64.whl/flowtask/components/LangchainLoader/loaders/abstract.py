from abc import ABC, abstractmethod
from typing import Union, List, Optional
from collections.abc import Callable
from datetime import datetime
from pathlib import PurePath
import torch
from langchain.docstore.document import Document
from navconfig.logging import logging
from navigator.libs.json import JSONContent  # pylint: disable=E0611
from ....conf import EMBEDDING_DEVICE


class AbstractLoader(ABC):
    """
    Abstract class for Document loaders.
    """
    def __init__(
        self,
        tokenizer: Union[str, Callable] = None,
        text_splitter: Union[str, Callable] = None,
        summarizer: Union[str, Callable] = None,
        markdown_splitter: Union[str, Callable] = None,
        source_type: str = 'file',
        doctype: Optional[str] = 'document',
        device: str = None,
        cuda_number: int = 0,
        llm: Callable = None,
        **kwargs
    ):
        self.tokenizer = tokenizer
        self._summary_model = summarizer
        self.text_splitter = text_splitter
        self.markdown_splitter = markdown_splitter
        self.doctype = doctype
        self.logger = logging.getLogger(
            f"Loader.{self.__class__.__name__}"
        )
        self._source_type = source_type
        # LLM (if required)
        self._llm = llm
        # JSON encoder:
        self._encoder = JSONContent()
        self.device_name = device
        self.cuda_number = cuda_number
        self._device = None
        self.encoding: str = kwargs.get('encoding', 'utf-8')

    async def __aenter__(self):
        # Cuda Device:
        self._device = self._get_device(
            self.device_name,
            self.cuda_number
        )
        return self

    async def __aexit__(self, *exc_info):
        self.post_load()

    def post_load(self):
        self.tokenizer = None  # Reset the tokenizer
        self.text_splitter = None  # Reset the text splitter
        torch.cuda.synchronize()  # Wait for all kernels to finish
        torch.cuda.empty_cache()  # Clear unused memory

    def _get_device(self, device_type: str = None, cuda_number: int = 0):
        """Get Default device for Torch and transformers.

        """
        if device_type == 'cpu':
            return torch.device('cpu')
        elif device_type == 'cuda':
            return torch.device(f'cuda:{cuda_number}')
        else:
            if torch.cuda.is_available():
                # Use CUDA GPU if available
                return torch.device(f'cuda:{cuda_number}')
            if torch.backends.mps.is_available():
                # Use CUDA Multi-Processing Service if available
                return torch.device("mps")
            if EMBEDDING_DEVICE == 'cuda':
                return torch.device(f'cuda:{cuda_number}')
            else:
                return torch.device(EMBEDDING_DEVICE)

    @abstractmethod
    async def load(self, path: PurePath) -> List[Document]:
        """Load data from a source and return it as a Langchain Document.

        Args:
            path (str): The source of the data.

        Returns:
            List[Document]: A list of Langchain Documents.
        """
        pass

    def create_metadata(
        self,
        path: Union[str, PurePath],
        doctype: str = 'document',
        source_type: str = 'source',
        doc_metadata: Optional[dict] = None,
        summary: Optional[str] = None
    ):
        if not doc_metadata:
            doc_metadata = {}
        if isinstance(path, PurePath):
            origin = path.name
            url = ''
            filename = path
        else:
            origin = path
            url = path
            filename = ''
        metadata = {
            "url": url,
            "source": origin,
            "filename": str(filename),
            "type": doctype,
            "question": '',
            "answer": '',
            "source_type": source_type,
            "created_at": datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            "document_meta": {
                **doc_metadata
            }
        }
        if summary:
            metadata['summary'] = summary
        return metadata

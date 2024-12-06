import asyncio
from typing import List
from collections.abc import Callable
from pathlib import Path, PurePath
from langchain.docstore.document import Document
from langchain.text_splitter import MarkdownTextSplitter
from ..flow import FlowComponent
from ...exceptions import ConfigError, ComponentError
from .loaders import MSWordLoader


class LangchainLoader(FlowComponent):
    """LangchainLoader.

    Overview:

    Getting a list of documents and convert into Langchain Documents.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.extensions: list = kwargs.pop('extensions', ['.txt'])
        self.encoding: str = kwargs.get('encoding', 'utf-8')
        self.path: str = kwargs.pop('path', None)
        self.skip_directories: List[str] = kwargs.pop('skip_directories', [])
        self._chunk_size = kwargs.get('chunk_size', 2048)
        self._embed_size: int = kwargs.pop('embed_size', 768)
        self.source_type: str = kwargs.pop('source_type', 'document')
        self.doctype: str = kwargs.pop('doctype', 'document')
        # LLM (if required)
        self._llm = kwargs.pop('llm', None)
        # Traslation Model:
        # Tokenizer Model:
        # Text Splitter Model:
        # Summarization Model:
        # Markdown Text Splitter:
        self._md_splitter = MarkdownTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=10
        )
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        self._device: str = kwargs.get('device', 'cpu')
        self._cuda_number: int = kwargs.get('cuda_device', 0)
        # Use caching to avoid instanciate several times same loader
        self._caching_loaders: dict = {}

    async def close(self):
        # Destroy effectively all Models.
        pass

    async def start(self, **kwargs):
        await super().start(**kwargs)
        if self.path:
            if isinstance(self.path, str):
                self.path = self.mask_replacement_recursively(self.path)
                self.path = Path(self.path).resolve()
                if not self.path.exists():
                    raise ComponentError(
                        f"Langchain: {self.path} doesn't exists."
                    )
        else:
            raise ConfigError(
                "Provide at least one directory or filename in *path* attribute."
            )

    def _get_loader(self, suffix):
        """
        Get a Document Loader based on Prefix.
        TODO: a more automated way using importlib.
        """
        # Common Arguments
        args = {
            "markdown_splitter": self._md_splitter,
            "device": self._device,
            "cuda_number": self._cuda_number,
            "source_type": self.source_type,
            "encoding": self.encoding,
            "llm": self._llm
        }
        if suffix == '.docx':
            return MSWordLoader(
                **args
            )

    async def _load_document(self, path: PurePath) -> List[Document]:
        documents = []
        suffix = path.suffix
        if suffix in self._caching_loaders:
            loader = self._caching_loaders[suffix]
        else:
            loader = self._get_loader(suffix)
            self._caching_loaders[suffix] = loader
        async with loader as ld:
            documents = await ld.load(path)
        # split or not split?
        return documents

    async def run(self):
        documents = []
        if self.path.is_dir():
            # iterate over the files in the directory
            if self.extensions:
                for ext in self.extensions:
                    for item in self.path.glob(f'*{ext}'):
                        if item.is_file() and set(item.parts).isdisjoint(self.skip_directories):
                            documents.extend(await self._load_document(item))
            else:
                for item in self.path.glob('*.*'):
                    if item.is_file() and set(item.parts).isdisjoint(self.skip_directories):
                        documents.extend(await self._load_document(item))
        elif self.path.is_file():
            if self.path.suffix in self.extensions:
                if set(self.path.parts).isdisjoint(self.skip_directories):
                    documents = await self._load_document(self.path)
        else:
            raise ValueError(
                f"Langchain Loader: Invalid path: {self.path}"
            )
        self._result = documents
        self.add_metric('DOCUMENTS', documents)
        return self._result

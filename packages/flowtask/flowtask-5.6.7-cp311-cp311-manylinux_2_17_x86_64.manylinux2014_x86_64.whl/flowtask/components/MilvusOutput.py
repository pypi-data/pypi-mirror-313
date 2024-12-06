"""
Milvus Database Vectorstore Output.
"""
from collections.abc import Callable
import asyncio
from .flow import FlowComponent
from ..exceptions import DataNotFound, ComponentError, ConfigError
from ..interfaces.vectorstores import MilvusStore


class MilvusOutput(MilvusStore, FlowComponent):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.upsert: bool = kwargs.pop('upsert', True)
        self.pk: str = kwargs.pop('pk', 'source_type')
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        await super().start(**kwargs)
        self.processing_credentials()
        if not self.credentials:
            raise ConfigError(
                "Unable to find valid Credentials for Milvus DB."
            )
        if not self.data:
            raise DataNotFound(
                "List of Documents is Empty."
            )
        if not isinstance(self.data, list):
            raise ComponentError(
                f"Incompatible kind of data received, expected *list*, receives {type(self.data)}"
            )
        return True

    async def close(self):
        pass

    async def run(self):
        """
        Saving Langchain Documents on a Milvus Database.
        """
        # Connecting to Milvus
        # TODO: add Collection creation:
        self._result = None
        async with self as connection:
            vector, documents = await connection.load_documents(
                self.data,
                collection=self.collection_name,
                upsert=self.upsert,
                pk=self.pk
            )
            result = {
                "vectorstore": vector,
                "documents": documents
            }
            self._result = result
        self.add_metric('DOCUMENTS_LOADED', len(self.data))
        self.add_metric('DOCUMENTS', documents)
        return result

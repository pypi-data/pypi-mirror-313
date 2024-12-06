import os
from collections.abc import Callable
import asyncio
from ..utils import SafeDict
from .flow import FlowComponent
from ..exceptions import ComponentError
from ..interfaces.qs import QSSupport


class CopyTo(QSSupport, FlowComponent):
    """CopyTo.

    Abstract Class for Copying (saving) a Pandas Dataframe onto a Resource
    (example: Copy to PostgreSQL).
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.pk = []
        self.truncate: bool = False
        self.data = None
        self._engine = None
        self.tablename: str = ""
        self.schema: str = ""
        self.use_chunks = False
        self.chunksize = None
        self._connection: Callable = None
        self._driver: str = kwargs.pop('driver', 'pg')
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        super(CopyTo, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "CopyTo: Data Was Not Found"
            )
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                val = value.format_map(SafeDict(**self._variables))
                object.__setattr__(self, attr, val)
        if not self.schema:
            try:
                self.schema = self._program
            except (ValueError, AttributeError, TypeError) as ex:
                raise ComponentError(
                    "CopyTo: Schema name not defined."
                ) from ex
        # Getting the connection, DSN or credentials:
        self._connection = await self.create_connection(
            driver=self._driver
        )

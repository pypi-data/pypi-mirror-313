import asyncio
from typing import Dict, List
from collections.abc import Callable
from navconfig.logging import logging
from asyncdb.exceptions import ProviderError
from ..exceptions import DataNotFound, ComponentError
from ..conf import TASK_PATH
from .flow import FlowComponent
from .DbClient import DbClient
from ..interfaces import TemplateSupport


class DataInput(DbClient, FlowComponent, TemplateSupport):
    """
    DataInput

    Class to execute queries against a database and retrieve results using asyncDB.

    Inherits from both `DbClient` (for database connection management) and
    `FlowComponent` (for component lifecycle management).

    .. table:: Properties
    :widths: auto

        +---------------+----------+------------------------------------------------------------------------------+
        | Name          | Required | Description                                                                  |
        +---------------+----------+------------------------------------------------------------------------------+
        | driver        |   Yes    | asyncDB driver to use (defaults to "pg" for PostgreSQL).                     |
        |               |          | Can be overridden by a "driver" key in the "credentials" dictionary.         |
        +---------------+----------+------------------------------------------------------------------------------+
        | credentials   |   Yes    | Dictionary containing database connection credentials (user, password, etc.).|
        +---------------+----------+------------------------------------------------------------------------------+
        | query         |   Yes    | SQL query or queries to be executed. Can be provided in different formats:   |
        |               |          |  * String (single query)                                                     |
        |               |          |  * List (multiple queries)                                                   |
        |               |          |  * Dictionary (named queries) - key-value pairs where key is the query name  |
        |               |          |    and value is the query string.                                            |
        |               |          | If not provided, no queries will be executed.                                |
        +---------------+----------+------------------------------------------------------------------------------+
        | file          |   Yes    | Path to a file containing a single or multiple SQL queries (alternative to   |
        |               |          | `query`).                                                                    |
        |               |          | If provided along with `query`, `file` takes precedence.                     |
        +---------------+----------+------------------------------------------------------------------------------+
        | as_dataframe  |    No    | Boolean flag indicating whether to convert query results to DataFrames.      |
        |               |          | Defaults to False (returns raw results).                                     |
        +---------------+----------+------------------------------------------------------------------------------+

    .. returns::
      The return value depends on the number of queries executed and the `as_dataframe` property:
         * **Single Query:**
             * DataFrame (if `as_dataframe` is True): Pandas DataFrame containing the query results.
             * raw result object (default): Raw result object specific to the database driver.
         * **Multiple Queries:**
             * List[DataFrame] (if `as_dataframe` is True): List of DataFrames, each corresponding to a query result.
             * List[raw result object] (default): List of raw result objects, each representing a query result.
      Returns None if no queries are provided.
    """  # noqa
    _credentials: dict = {
        "host": str,
        "port": int,
        "user": str,
        "password": str,
        "database": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.queries: List = []
        self.driver = kwargs.pop('driver', "pg")  # default driver
        kwargs['driver'] = self.driver
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        if self.credentials and "driver" in self.credentials:
            self.driver = self.credentials.pop('driver')

    async def start(self, **kwargs) -> bool:
        await super(DataInput, self).start(**kwargs)
        self.queries = []
        if hasattr(self, "query"):
            if isinstance(self.query, str):  # sigle query # pylint: disable=E0203
                self.query = self.mask_replacement(self.query)
                self.queries.append(self.query)
            elif isinstance(self.query, list):  # multiple queries:
                for query in self.query:
                    query = self.mask_replacement(query)
                    self.queries.append(query)
            elif isinstance(self.query, dict):  # named queries:
                for name, query in self.query.items():
                    qs = {}
                    query = self.mask_replacement(query)
                    qs[name] = query
                    self.queries.append(qs)
        elif hasattr(self, "file"):  # query from a File
            if isinstance(self.file, str):  # sigle query
                self._logger.debug(f"Execute SQL File: {self.file!s}")
                file_path = TASK_PATH.joinpath(self._program, "sql", self.file)
                qs = await self.open_sqlfile(file_path)
                self.queries.append(qs)
            elif isinstance(self.file, list):  # multiple queries:
                for file in self.file:
                    query = await self.open_sqlfile(file)
                    self.queries.append(qs)
        return True

    async def close(self):
        self.connection = None

    async def run(self):
        try:
            db = await self.connection(
                driver=self.driver, credentials=self.credentials
            )
        except Exception as e:
            logging.error(e)
            raise
        try:
            async with await db.connection() as conn:
                if conn.is_connected() is not True:
                    raise ComponentError(
                        f"DB Error: driver {self.driver} is not connected."
                    )
                results = []
                for query in self.queries:
                    if isinstance(query, str):
                        result = await self._query(query, conn)
                        rst = len(result)
                        st = {"query": query, "result": rst}
                        self.add_metric(f"Query: {query}", st)
                        if self.as_dataframe is True:
                            # converting to a dataframe
                            df = await self.get_dataframe(result)
                            results.append(df)
                        else:
                            results.append(result)
                    elif isinstance(query, dict):
                        qs = {}
                        [(key, value)] = query.items()
                        result = await self._query(value, conn)
                        rst = len(result)
                        st = {"query": query, "result": rst}
                        self.add_metric(f"Query: {key}", st)
                        if self.as_dataframe is True:
                            df = await self.get_dataframe(result)
                            qs[key] = df
                        else:
                            qs[key] = result
                        results.append(qs)
                if len(results) == 1:
                    self._result = results[0]
                else:
                    self._result = results
                return self._result
        except DataNotFound:
            raise
        except ProviderError as e:
            raise ComponentError(f"Error connecting to database: {e}") from e
        except Exception as e:
            logging.error(e)
            raise

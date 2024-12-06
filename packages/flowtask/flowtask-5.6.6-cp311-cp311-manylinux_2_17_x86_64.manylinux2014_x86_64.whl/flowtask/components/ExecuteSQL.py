import asyncio
from collections.abc import Callable
from pathlib import PurePath
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import aiofiles
from asyncdb.drivers.pg import pg
from asyncdb.exceptions import StatementError, DataError
from querysource.conf import (
    default_dsn,
    DB_TIMEOUT,
    DB_STATEMENT_TIMEOUT,
    DB_SESSION_TIMEOUT,
    DB_KEEPALIVE_IDLE
)
from navconfig.logging import logging
from ..exceptions import ComponentError, FileError
from ..utils import SafeDict
# TODO: migrate to FileStore component
from .flow import FlowComponent
from ..interfaces import TemplateSupport
from ..conf import TASK_PATH


class ExecuteSQL(FlowComponent, TemplateSupport):
    """
    ExecuteSQL

    Overview

        Executes one or more SQL queries against a PostgreSQL database, also can execute SQL's in a file.

    **Properties** (inherited from FlowComponent)

    .. table:: Properties
        :widths: auto

        +--------------+----------+-----------+-------------------------------------------------------+
        | Name         | Required | Summary                                                           |
        +--------------+----------+-----------+-------------------------------------------------------+
        | skipError    |   No     | The name of the database schema to use (default: "").             |
        +--------------+----------+-----------+-------------------------------------------------------+
        | sql          |   No     | A raw SQL query string to execute.                                |
        +--------------+----------+-----------+-------------------------------------------------------+
        | file_sql     |   No     | A path (string) or list of paths (strings) to SQL files           |
        |              |          | containing the queries to execute.                                |
        +--------------+----------+-----------+-------------------------------------------------------+
        | pattern      |   No     | A dictionary mapping variable names to functions that return      |
        |              |          | the corresponding values to be used in the SQL query.             |
        +--------------+----------+-----------+-------------------------------------------------------+
        | use_template |   No     | Whether to treat the SQL string as a template and use the         |
        |              |          | `_templateparser` component to render it (default: False).        |
        +--------------+----------+-----------+-------------------------------------------------------+
        | multi        |   No     | Whether to treat the `sql` property as a list of multiple         |
        |              |          | queries to execute sequentially (default: False).                 |
        +--------------+----------+-----------+-------------------------------------------------------+
        | exec_timeout |   No     | The timeout value for executing a single SQL query                |
        |              |          | (default: 3600 seconds).                                          |
        +--------------+----------+-----------+-------------------------------------------------------+
    **Methods**

    * open_sqlfile(self, file: PurePath, **kwargs) -> str: Opens an SQL file and returns its content.
    * get_connection(self, event_loop: asyncio.AbstractEventLoop): Creates a connection pool to the PostgreSQL database.
    * _execute(self, query, event_loop): Executes a single SQL query asynchronously.
    * execute_sql(self, query: str, event_loop: asyncio.AbstractEventLoop) -> str: Executes an SQL query and returns the result.

    **Notes**

    * This component uses asynchronous functions for non-blocking I/O operations.
    * Error handling is implemented to catch exceptions during database connection, SQL execution, and file operations.
    * Supports loading SQL queries from files.
    * Supports using templates for dynamic SQL generation.
    * Supports executing multiple queries sequentially.
    """  # noqa
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.tablename: str = ""
        self.schema: str = ""
        self._connection: Callable = None
        self._queries = []
        self.exec_timeout: float = kwargs.pop(
            "exec_timeout", 3600000.0
        )
        self.multi: bool = bool(kwargs.get("multi", False))
        self.use_template: bool = bool(kwargs.get('use_template', False))
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        # set the program:
        if hasattr(self, "program"):
            self._program = self.program

    async def close(self):
        """Closing Database Connection."""
        pass

    async def open_sqlfile(self, file: PurePath, **kwargs) -> str:
        content = None
        self._logger.info(f"Open SQL File: {file}")
        if file.exists() and file.is_file():
            # open SQL File:
            async with aiofiles.open(file, "r+") as afp:
                content = await afp.read()
                # check if we need to replace masks
                if "{" in content:
                    content = self.mask_replacement(content)
            if self.use_template is True:
                content = self._templateparser.from_string(content, kwargs)
            return content
        else:
            raise FileError(f"ExecuteSQL: Missing SQL File: {file}")

    async def start(self, **kwargs):
        """Start Component"""
        if self.previous:
            self.data = self.input
        # check if sql comes from a filename:
        if hasattr(self, "file_sql"):
            self._logger.debug(f"SQL File: {self.file_sql}")
            self._queries = []
            qs = []
            if isinstance(self.file_sql, str):
                qs.append(self.file_sql)
            elif isinstance(self.file_sql, list):
                qs = self.file_sql
            else:
                raise ComponentError(
                    "ExecuteSQL: Unknown type for *file_sql* attribute."
                )
            for fs in qs:
                self._logger.debug(f"Execute SQL File: {fs!s}")
                file_path = TASK_PATH.joinpath(self._program, "sql", fs)
                try:
                    sql = await self.open_sqlfile(file_path)
                    self._queries.append(sql)
                except Exception as err:
                    raise ComponentError(f"{err}") from err
        if hasattr(self, "pattern"):
            # need to parse variables in SQL
            pattern = self.pattern
            self._queries = []
            try:
                variables = {}
                for field, val in pattern.items():
                    variables[field] = self.getFunc(val)
            except (TypeError, AttributeError) as err:
                self._logger.error(err)
            # replace all ocurrences on SQL
            try:
                # TODO: capture when sql is a list of queries
                sql = self.sql.format_map(SafeDict(**variables))
                # Replace variables
                for val in self._variables:
                    if isinstance(self._variables[val], list):
                        if isinstance(self._variables[val], int):
                            self._variables[val] = ", ".join(self._variables[val])
                        else:
                            self._variables[val] = ", ".join(
                                "'{}'".format(v) for v in self._variables[val]
                            )
                    sql = sql.replace(
                        "{{{}}}".format(str(val)), str(self._variables[val])
                    )
                self._queries.append(sql)
            except Exception as err:
                logging.exception(err, stack_info=True)
        if hasattr(self, "sql"):
            if isinstance(self.sql, str):
                self._queries = [self.sql]
            elif isinstance(self.sql, list):
                self._queries = self.sql
        # Replace variables
        for val in self._variables:
            sqls = []
            for sql in self._queries:
                if isinstance(self._variables[val], list):
                    if isinstance(self._variables[val], int):
                        self._variables[val] = ", ".join(self._variables[val])
                    else:
                        self._variables[val] = ", ".join(
                            "'{}'".format(v) for v in self._variables[val]
                        )
                sql = sql.replace("{{{}}}".format(str(val)), str(self._variables[val]))
                sqls.append(sql)
            self._queries = sqls
        return True

    def get_connection(self, event_loop: asyncio.AbstractEventLoop):
        kwargs: dict = {
            "min_size": 2,
            "server_settings": {
                "application_name": "FlowTask.ExecuteSQL",
                "client_min_messages": "notice",
                "max_parallel_workers": "512",
                "jit": "off",
                # "statement_timeout": f"{DB_STATEMENT_TIMEOUT}",
                # "idle_session_timeout": f"{DB_SESSION_TIMEOUT}",
                "effective_cache_size": "2147483647",
                "tcp_keepalives_idle": f"{DB_KEEPALIVE_IDLE}",
            },
        }
        return pg(dsn=default_dsn, loop=event_loop, timeout=int(DB_TIMEOUT), **kwargs)

    async def _execute(self, query, event_loop):
        try:
            connection = self.get_connection(event_loop)
            async with await connection.connection() as conn:
                if hasattr(self, "background"):
                    future = asyncio.create_task(conn.execute(query))
                    # query will be executed in background
                    _, pending = await asyncio.wait(
                        [future], timeout=self.exec_timeout, return_when="ALL_COMPLETED"
                    )
                    if future in pending:
                        ## task reachs timeout
                        for t in pending:
                            t.cancel()
                        raise asyncio.TimeoutError(
                            f"Query {query!s} was cancelled due timeout."
                        )
                    result, error = future.result()
                else:
                    try:
                        result, error = await conn.execute(query)
                    except asyncio.TimeoutError as exc:
                        raise asyncio.TimeoutError(
                            f"Query {query!s} was cancelled due Timeout."
                        ) from exc
                    except Exception as exc:
                        raise ComponentError(f"ExecuteSQL Error: {exc!s}") from exc
                if error:
                    raise ComponentError(
                        f"Execute SQL error: {result!s} err: {error!s}"
                    )
                else:
                    return result
        except StatementError as err:
            raise StatementError(f"Statement error: {err}") from err
        except DataError as err:
            raise DataError(f"Data error: {err}") from err
        except ComponentError:
            raise
        except Exception as err:
            raise ComponentError(f"ExecuteSQL error: {err}") from err
        finally:
            connection = None

    def execute_sql(self, query: str, event_loop: asyncio.AbstractEventLoop) -> str:
        asyncio.set_event_loop(event_loop)
        if self._debug:
            self._logger.verbose(f"::: Exec SQL: {query}")
        future = event_loop.create_task(self._execute(query, event_loop))
        try:
            result = event_loop.run_until_complete(future)
            st = {"sql": query, "result": result}
            self.add_metric("EXECUTED", st)
            return result
        except Exception as err:
            self.add_metric("QUERY_ERROR", str(err))
            self._logger.error(f"{err}")

    async def run(self):
        """Run Raw SQL functionality."""
        try:
            _new = True
            event_loop = asyncio.new_event_loop()
        except RuntimeError:
            event_loop = asyncio.get_running_loop()
            _new = False
        ct = len(self._queries)
        if ct <= 0:
            ct = 1
        result = []
        try:
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
            with ThreadPoolExecutor(max_workers=ct) as executor:
                for query in self._queries:
                    fn = partial(self.execute_sql, query, event_loop)
                    res = await loop.run_in_executor(executor, fn)
                    result.append(res)
        except ComponentError:
            raise
        except Exception as err:
            raise ComponentError(f"{err}") from err
        finally:
            try:
                if _new is True:
                    event_loop.close()
            except Exception:
                pass
        # returning the previous data:
        if self.data is not None:
            self._result = self.data
        else:
            self._result = result
        return self._result

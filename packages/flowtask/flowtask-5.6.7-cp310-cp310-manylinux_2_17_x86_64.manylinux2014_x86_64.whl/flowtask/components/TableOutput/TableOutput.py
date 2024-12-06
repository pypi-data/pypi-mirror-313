import asyncio
import logging
from collections.abc import Callable
from sqlalchemy.exc import NoSuchTableError
import pandas as pd
from querysource.queries.multi.outputs import (
    PgOutput,
    MysqlOutput,
    SaOutput,
    RethinkOutput,
    BigQueryOutput,
)
from ...exceptions import ComponentError, DataNotFound
from ..flow import FlowComponent
from ...utils import AttrDict
from ...utils.functions import is_empty
from ...interfaces.credentials import CredentialsInterface


class TableOutput(FlowComponent, CredentialsInterface):
    """
    TableOutput

    Overview

        The TableOutput class is a component for copying data to SQL tables using Pandas and SQLAlchemy features. It supports
        various SQL flavors such as PostgreSQL, MySQL, and SQLAlchemy. The class handles data type detection, data transformation,
        and the INSERT-UPDATE mechanism.

    .. table:: Properties
    :widths: auto

        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | Name             | Required | Description                                                                                      |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _pk              |   No     | A list of primary keys for the table.                                                            |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _fk              |   No     | The foreign key for the table.                                                                   |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | data             |   Yes    | The data to be copied to the table.                                                              |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _engine          |   Yes    | The database engine used for the SQL operations.                                                 |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _columns         |   No     | A list of columns in the table.                                                                  |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _schema          |   No     | The schema of the table.                                                                         |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _constraint      |   No     | A list of constraints for the table.                                                             |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | _dsn             |   Yes    | The data source name (DSN) for the database connection.                                          |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | flavor           |   Yes    | The SQL flavor for the database, defaults to "postgresql".                                       |
        +------------------+----------+--------------------------------------------------------------------------------------------------+
        | multi            |   No     | A flag indicating if multiple DataFrame transformations are supported, defaults to False.        |
        +------------------+----------+--------------------------------------------------------------------------------------------------+

        Returns:
            DataFrame: The data that was copied to the table.
    """  # noqa

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._pk = []
        self._fk: str = None
        self._engine = None
        self._columns: list = []
        self._schema: str = ""
        self._constraint: list = None
        dsn = kwargs.get('dsn', None)
        self.data = kwargs.get('data', None)
        self.tablename = kwargs.pop('tablename', None)
        if self.tablename is None:
            self.tablename = kwargs.pop('table', None)
        if dsn is not None and dsn.startswith('postgres:'):
            dsn = dsn.replace('postgres:', 'postgresql:')
        # DB Flavor
        self.flavor: str = kwargs.pop('flavor', 'postgresql')
        self.multi: bool = bool(kwargs.pop('multi', False))
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # get DSN:
        self._dsn = self.get_env_value(dsn, default=dsn)

    def constraints(self):
        return self._constraint

    def get_schema(self):
        return self._schema

    def foreign_keys(self):
        return self._fk

    def primary_keys(self):
        return self._pk

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            if is_empty(self.data):
                raise DataNotFound(
                    "Previous Data was Not Found"
                )
        await super(TableOutput, self).start(**kwargs)
        args = {}
        if hasattr(self, "do_update"):
            args = {"do_update": self.do_update}
        if self.flavor in ("postgres", "postgresql"):
            self._engine = PgOutput(parent=self, external=False, **args)
        elif self.flavor == "mysql":
            self._engine = MysqlOutput(parent=self, dsn=self._dsn, external=False)
        elif self.flavor == "sqlalchemy":
            self._engine = SaOutput(parent=self, dsn=self._dsn, external=False)
        elif self.flavor in ("rethinkdb", "rethink"):
            self._engine = RethinkOutput(parent=self, external=True)
        elif self.flavor in ("bigquery", "bq"):
            self._engine = BigQueryOutput(parent=self, external=True)
        else:
            raise ComponentError(
                f"TableOutput: unsupported DB flavor: {self.flavor}"
            )
        if self.data is None:
            raise DataNotFound(
                "TableOutput: Data missing"
            )
        elif isinstance(self.data, pd.DataFrame):
            # detect data type for colums
            columns = list(self.data.columns)
            for column in columns:
                t = self.data[column].dtype
                # print(column, '->', t, '->', self.data[column].iloc[0])
                if isinstance(t, pd.core.dtypes.dtypes.DatetimeTZDtype):
                    self.data[column] = pd.to_datetime(
                        self.data[column],
                        format="%Y-%m-%dT%H:%M:%S.%f%z",
                        cache=True,
                        utc=True,
                    )
                    self.data[column].dt.tz_convert("UTC")
                elif str(t) == "datetime64[ns]":
                    tmp_data = self.data.copy()
                    tmp_data[column] = pd.to_datetime(
                        self.data[column],
                        format="%Y-%m-%dT%H:%M:%S.%f%z",
                        cache=True,
                        utc=True,
                    )
                    self.data = tmp_data.copy()
                else:
                    # this is an special column from RethinkDB
                    # rethinkdb.ast.RqlTzinfo
                    if column == "inserted_at":
                        try:
                            self.data[column] = pd.to_datetime(
                                self.data[column],
                                format="%Y-%m-%dT%H:%M:%S.%f%z",
                                cache=True,
                                utc=True,
                            )
                        except ValueError:
                            self.data[column] = pd.to_datetime(
                                self.data[column],
                                # format='%Y-%m-%d %H:%M:%S.%f+%z',
                                cache=True,
                                utc=True,
                            )
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    f"Invalid Result type for Multiple: {err}"
                ) from err
            for name, rs in result:
                if hasattr(self, name):
                    el = getattr(self, name)
                    print(el)
                    if not isinstance(rs, pd.DataFrame):
                        raise ComponentError("Invalid Resultset: not a Dataframe")
        return True

    def close(self):
        """Closing Operations."""
        try:
            self._engine.close()
        except Exception as err:
            logging.error(err)

    async def table_output(self, elem, datasource):
        # get info
        options = {"chunksize": 100}
        table = elem.tablename
        try:
            schema = elem.schema
        except AttributeError:
            schema = "public"
        # starting metric:
        try:
            data = {"NUM_ROWS": datasource.shape[0], "NUM_COLUMNS": datasource.shape[1]}
            self.add_metric(f"{schema}.{table}", data)
        except Exception:
            pass
        if self._engine.is_external is False:
            options["schema"] = schema
            if hasattr(elem, "sql_options"):
                options = {**options, **elem.sql_options}
            if hasattr(elem, "pk") or hasattr(elem, "constraint"):
                options["index"] = False
            if hasattr(elem, "if_exists"):
                options["if_exists"] = elem.if_exists
            else:
                options["if_exists"] = "append"
            # define index:
            try:
                self._pk = elem.pk
                options["index_label"] = self._pk
            except AttributeError:
                self._pk = []
            # set the upsert method:
            options["method"] = self._engine.db_upsert
            if hasattr(elem, "foreign_key"):
                self._fk = elem.foreign_key
            else:
                self._fk = None
            if hasattr(elem, "constraint"):
                self._constraint = elem.constraint
            else:
                self._constraint = None
            self._columns = list(datasource.columns)
            self._engine.columns = self._columns
            self._schema = schema
            # add metrics for Table Output
            u = datasource.select_dtypes(include=["object", "string"])
            datasource[u.columns] = u.replace(["<NA>", "None"], None)
            try:
                datasource.to_sql(name=table, con=self._engine.engine(), **options)
                logging.debug(f":: Saving Table Data {schema}.{table} ...")
                return True
            except NoSuchTableError as exc:
                raise ComponentError(f"There is no Table {table}: {exc}") from exc
            except Exception as exc:
                raise ComponentError(f"{exc}") from exc
        else:
            # Using Engine External method write:
            on_conflict = 'replace'
            if hasattr(elem, 'if_exists'):
                on_conflict = elem.if_exists
            await self._engine.db_upsert(  # pylint: disable=E1120,E1123 # noqa
                table=table, schema=schema, on_conflict=on_conflict, data=datasource
            )  # pylint: disable=E1120,E1123 # noqa

    async def run(self):
        """Run TableOutput."""
        try:
            self._result = None
            if self.multi is False:
                # set the number of rows:
                self._variables["{self.StepName}_NUMROWS"] = len(self.data.index)
                await self.table_output(self, self.data)
                self._result = self.data
                try:
                    self.add_metric("ROWS_SAVED", len(self.data.index))
                except (TypeError, ValueError):
                    pass
                return self._result
            else:
                # running in multi Mode
                try:
                    result = self.data.items()
                except Exception as err:
                    raise ComponentError(
                        f"Invalid Result type for Multiple: {err}"
                    ) from err
                for name, rs in result:
                    try:
                        el = getattr(self, name)
                    except AttributeError:
                        continue
                    await self.table_output(AttrDict(el), rs)
                    # set the number of rows:
                    self._variables[f"{self.StepName}_{name}_NUMROWS"] = len(rs.index)
                # return the same dataframe
                self._result = self.data
                try:
                    self.add_metric("ROWS_SAVED", self._engine.result())
                except Exception as err:
                    logging.error(err)
                return self._result
        except ValueError as err:
            raise ComponentError(f"Value Error: {err}") from err
        except Exception as err:
            raise ComponentError(f"TableOutput: {err}") from err

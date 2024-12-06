import asyncio
from typing import Callable
import pandas as pd
from asyncdb.models import Model
from querysource.datasources.drivers.bigquery import bigquery_default
from ..utils import SafeDict
from .flow import FlowComponent
from ..exceptions import ComponentError, DriverError, DataNotFound
from ..interfaces.qs import QSSupport


# Define the primary key SQL statement template for BigQuery
pk_sentence = """
ALTER TABLE `{schema}.{table}`
ADD CONSTRAINT `{schema}_{table}_pkey` PRIMARY KEY({fields});
"""

class CopyToBigQuery(QSSupport, FlowComponent):
    """
    CopyToBigQuery.

    Overview

        This component allows copying data from a Pandas DataFrame to a BigQuery table
        using the write functionality from the Querysource BigQuery driver.

    .. table:: Properties
       :widths: auto

    +--------------+----------+--------------------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+--------------------------------------------------------+
    | tablename    |   Yes    | Name of the table in the BigQuery dataset              |
    +--------------+----------+--------------------------------------------------------+
    | schema       |   Yes    | Name of the BigQuery dataset                          |
    +--------------+----------+--------------------------------------------------------+
    | truncate     |   Yes    | Indicates if the component should empty               |
    |              |          | the table before copying new data. If set to true,      |
    |              |          | the table will be truncated before saving the new data.|
    +--------------+----------+--------------------------------------------------------+
    | use_chunks   |   No     | When activated, allows inserting data in chunks to    |
    |              |          | optimize performance with large datasets.             |
    +--------------+----------+--------------------------------------------------------+
    | chunksize    |   No     | Defines the size of each chunk when `use_chunks` is    |
    |              |          | enabled.                                               |
    +--------------+----------+--------------------------------------------------------+
    | credentials  |   No     | Path to the BigQuery credentials JSON file.            |
    +--------------+----------+--------------------------------------------------------+
    | datasource   |   No     | Using a Datasource instead of manual credentials       |
    |              |          | (if applicable).                                       |
    +--------------+----------+--------------------------------------------------------+
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
        self.tablename: str = ""
        self.schema: str = ""
        self.use_chunks = False
        self.chunksize = 10000  # Default chunk size
        self._connection = None
        self._driver: str = kwargs.pop('driver', 'bigquery')  # Default driver to 'bigquery'
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        super(CopyToBigQuery, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def close(self):
        pass

    async def start(self, **kwargs):
        """Initialize the component by obtaining the DataFrame and setting up the connection."""
        # Obtain the input DataFrame
        if self.previous:
            self.data = self.input
        else:
            raise DataNotFound("CopyToBigQuery: No input DataFrame found.")

        # Format string attributes with variables
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                val = value.format_map(SafeDict(**self._variables))
                object.__setattr__(self, attr, val)

        # Validate that schema is defined
        if not self.schema:
            try:
                self.schema = self._program
            except (ValueError, AttributeError, TypeError) as ex:
                raise ComponentError("CopyToBigQuery: Schema name not defined.") from ex

        # Establish connection to BigQuery using AsyncDB
        self._connection = await self.create_connection(driver=self._driver)

    async def run(self):
        """Execute the copy operation to BigQuery."""
        self._result = None
        if self.data is None or self.data.empty:
            raise DataNotFound("CopyToBigQuery Error: No data in the DataFrame.")

        self._result = self.data
        columns = list(self.data.columns)
        self.add_metric("NUM_ROWS", self.data.shape[0])
        self.add_metric("NUM_COLUMNS", self.data.shape[1])

        if self._debug:
            self._logger.debug("Debugging: COPY TO BigQuery ===")
            for column in columns:
                dtype = self.data[column].dtype
                self._logger.debug(f"{column} -> {dtype} -> {self.data[column].iloc[0]}")

        # Create the BigQuery table if necessary
        if hasattr(self, "create_table"):
            await self.create_bigquery_table()

        # Truncate the table if specified
        if self.truncate:
            await self.truncate_table()

        # Insert data into BigQuery
        if isinstance(self.data, pd.DataFrame):
            if self.use_chunks:
                await self.insert_data_in_chunks(columns)
            else:
                await self.insert_data_directly(columns)
        else:
            # Handle other data types if necessary
            raise ComponentError("CopyToBigQuery: Input data type is not a DataFrame.")

        self._logger.debug(f"CopyToBigQuery: Saving results into: {self.schema}.{self.tablename}")
        return self._result

    async def close(self):
        """Close the connection to BigQuery."""
        try:
            if self._connection:
                await self._connection.close()
                self._logger.info("CopyToBigQuery: Connection to BigQuery closed.")
        except Exception as err:
            self._logger.error(f"CopyToBigQuery: Error closing connection: {err}")

    async def create_bigquery_table(self):
        """Create the table in BigQuery if it does not exist."""
        try:
            if hasattr(self, "create_table"):
                _pk = self.create_table.get("pk", None)
                _drop = self.create_table.get("drop", False)
                if _pk is None:
                    raise ComponentError(f"CopyToBigQuery: Primary key not defined for {self.schema}.{self.tablename}.")

                # Extract columns and data types
                columns = self.data.columns.tolist()
                cols = []
                for col in columns:
                    datatype = self.data[col].dtype
                    try:
                        t = self.map_dtype(datatype)
                    except KeyError:
                        t = "STRING"  # Default type
                    cols.append((col, t))

                # Create the model and generate the SQL statement
                cls = Model.make_model(name=self.tablename, schema=self.schema, fields=cols)
                mdl = cls()  # Empty model to get the schema
                sql = mdl.model(dialect="sql")
                if sql:
                    async with await self._connection.connection() as conn:
                        if _drop:
                            truncate_query = f"DROP TABLE IF EXISTS `{self.schema}.{self.tablename}`;"
                            await conn.execute(truncate_query)
                            self._logger.debug(f"CopyToBigQuery: Table {self.schema}.{self.tablename} dropped.")

                        # Create the table
                        await conn.execute(sql)
                        self._logger.debug(f"CopyToBigQuery: Table {self.schema}.{self.tablename} created.")

                        # Add primary key
                        pk_query = pk_sentence.format(
                            schema=self.schema,
                            table=self.tablename,
                            fields=",".join(_pk),
                        )
                        await conn.execute(pk_query)
                        self._logger.debug(f"CopyToBigQuery: Primary key added to {self.schema}.{self.tablename}.")
        except Exception as err:
            raise ComponentError(f"CopyToBigQuery: Error creating table {self.schema}.{self.tablename}: {err}") from err

    def map_dtype(self, dtype):
        """Map Pandas data types to BigQuery data types."""
        dtype_mapping = {
            'object': 'STRING',
            'int64': 'INTEGER',
            'float64': 'FLOAT',
            'bool': 'BOOLEAN',
            'datetime64[ns]': 'TIMESTAMP',
            'timedelta[ns]': 'TIMESTAMP',
            'category': 'STRING',
            'uint64': 'INTEGER',
            # Add more mappings as needed
        }
        return dtype_mapping.get(str(dtype), 'STRING')  # Default type

    async def truncate_table(self):
        """Truncate the table in BigQuery."""
        try:
            truncate_query = f"DELETE FROM `{self.schema}.{self.tablename}` WHERE TRUE;"
            await self._connection.execute(truncate_query)
            self._logger.debug(f"CopyToBigQuery: Table `{self.schema}.{self.tablename}` truncated.")
        except Exception as err:
            raise ComponentError(f"CopyToBigQuery: Error truncating table {self.schema}.{self.tablename}: {err}") from err

    async def insert_data_in_chunks(self, columns):
        """Insert data in chunks to handle large volumes."""
        try:
            for start in range(0, len(self.data), self.chunksize):
                chunk = self.data.iloc[start:start + self.chunksize]
                await self.insert_chunk(chunk, columns)
        except Exception as err:
            raise ComponentError(f"CopyToBigQuery: Error inserting data in chunks: {err}") from err

    async def insert_data_directly(self, columns):
        """Insert all data directly without using chunks."""
        try:
            await self.insert_chunk(self.data, columns)
        except Exception as err:
            raise ComponentError(f"CopyToBigQuery: Error inserting data directly: {err}") from err

    async def insert_chunk(self, chunk: pd.DataFrame, columns):
        """Insert a chunk of data into BigQuery using the write method."""
        if chunk.empty:
            self._logger.warning("CopyToBigQuery: Empty data chunk, skipping insertion.")
            return

        try:
            json_data = chunk.to_dict(orient='records')
            await self._connection.write(
                data=json_data,
                table_id=self.tablename,
                dataset_id=self.schema,
                if_exists="append"
            )
            self._logger.info(f"CopyToBigQuery: Inserted {len(json_data)} records into `{self.schema}.{self.tablename}`.")
            self.add_metric("ROWS_SAVED", len(json_data))
        except DriverError as e:
            self._logger.error(f"CopyToBigQuery: Error inserting chunk: {e}")
            raise ComponentError(f"CopyToBigQuery: Error inserting chunk: {e}") from e
        except Exception as e:
            self._logger.exception("CopyToBigQuery: Exception while inserting data chunk.")
            raise ComponentError(f"CopyToBigQuery: Exception inserting chunk: {e}") from e

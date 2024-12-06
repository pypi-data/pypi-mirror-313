import asyncio
from typing import Dict, Any
from collections.abc import Callable
from pathlib import PosixPath, Path
import re
from decimal import Decimal
import datetime
import numpy as np
import pandas as pd
import dask.dataframe as dd
from asyncdb.models import Model
import dateparser
from navconfig.logging import logging
from ..exceptions import FileError, ComponentError, DataNotFound
from .flow import FlowComponent
from ..interfaces import DBSupport
from ..utils.transformations import (
    is_camelcase,
    is_snakecase,
    remove_illegal_chars,
    camelcase_split
)
from ..utils.constants import excel_based


logging.getLogger("fsspec").setLevel(logging.CRITICAL)


dtypes = {
    "varchar": str,
    "character varying": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "integer": int,
    "bigint": np.int64,
    "int64": np.int64,
    "uint64": np.int64,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "date": datetime.date,
}


# adding support for primary keys on raw tables
pk_sentence = """ALTER TABLE {schema}.{table}
ADD CONSTRAINT {schema}_{table}_pkey PRIMARY KEY({fields});"""


def datetime_to_name(value: datetime.datetime, mask: str):
    return value.strftime(mask)


class TableSchema(DBSupport, FlowComponent):
    """
    TableSchema

        Overview

            The TableSchema class is a component for reading a CSV file or DataFrame and creating a table schema based 
            on data models. It supports various formatting and normalization options for column names, datatype inference,
            and automatic handling of primary keys. This component also supports normalization settings for column names,
            such as camelCase to snake_case conversion, illegal character removal, and customizable name replacements.

        .. table:: Properties
        :widths: auto

            +-------------------+----------+-----------+------------------------------------------------------------------+
            | Name              | Required | Summary                                                                      |
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | filename          |   Yes    | The CSV file or DataFrame input to read and infer schema from.               |
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | schema            |   No     | The database schema for the table.                                           |
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | tablename         |   Yes    | The name of the table to be created based on the data model.                 |
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | drop              |   No     | Boolean specifying if an existing table with the same name should be dropped.|
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | normalize_names   |   No     | Dictionary with options for column name normalization.                       |
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | pk                |   No     | List of columns to define as primary keys.                                   |
            +-------------------+----------+-----------+------------------------------------------------------------------+
            | replace_names     |   No     | Dictionary of column name replacements for renaming specific columns.        |
            +-------------------+----------+-----------+------------------------------------------------------------------+

        Returns

            This component returns the input data after creating a database table schema based on the data’s inferred or
            specified structure. If the input is a file, it reads and processes the file; if a DataFrame, it directly
            processes the DataFrame. The component provides detailed metrics on column structure and row counts, as well as
            logging for SQL execution status and any schema creation errors.
    """ # noqa

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        self.separator: str = ","
        self.params: Dict = {}
        self.fields: Dict = {}
        self.replace_names: Dict = {}
        self.drop: bool = False
        self.data: Any = None
        self.filename: str = None
        # info about table:
        self.tablename: str = None
        self.schema: str = None
        super(TableSchema, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            if isinstance(self.input, PosixPath):
                self.filename = self.input
            elif isinstance(self.input, list):
                self.filename = PosixPath(self.input[0])
            elif isinstance(self.input, str):
                self.filename = PosixPath(self.input)
            elif isinstance(self.input, dict):
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = PosixPath(filenames[0])
                    except IndexError as err:
                        raise FileError(f"File doesnt exists: {filenames}") from err
            elif isinstance(self.input, dd.DataFrame) or isinstance(
                self.input, pd.DataFrame
            ):
                self.filename = None
                self.data = self.input
            else:
                raise FileError(f"File doesnt exists: {self.input}")
        elif hasattr(self, "filename"):
            self.filename = Path(self.filename)
        else:
            raise ComponentError(
                "TableSchema: This Component requires a File or Dataframe from input."
            )
        await super().start(**kwargs)
        self.processing_credentials()

    async def close(self):
        pass

    def rename_repeated_col(self, col, cols):
        renamed = False
        count = 1
        for c, t in cols:
            if c == col:
                if not renamed:
                    col = f"{col}_{count}"
                    count += 1
                    renamed = True
                else:
                    col = col.split("_", 1)[0]
                    col = f"{col}_{count}"
                    count += 1
        return col

    async def run(self):
        self.result = None
        if not hasattr(self, "mime"):
            self.mime = "text/csv"
        if self.filename:
            if self.mime in excel_based:
                if (
                    self.mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ):
                    # xlsx or any openxml based document
                    file_engine = self.params.get("file_engine", "openpyxl")
                elif (
                    self.mime == "application/vnd.ms-excel.sheet.binary.macroEnabled.12"
                ):
                    file_engine = self.params.get("file_engine", "pyxlsb")
                else:
                    try:
                        ext = self.filename.suffix
                    except (AttributeError, ValueError):
                        ext = ".xls"
                    if ext == ".xls":
                        file_engine = self.params.get("file_engine", "xlrd")
                    else:
                        file_engine = self.params.get("file_engine", "openpyxl")
                # passed arguments to Pandas directly
                arguments = {**self.params}
                if hasattr(self, "pd_args") and isinstance(self.pd_args, dict):
                    arguments = {**self.params, **self.pd_args}
                df = pd.read_excel(
                    self.filename,
                    engine=file_engine,
                    keep_default_na=True,
                    na_filter=False,
                    **arguments,
                )
            else:
                self.params = {"infer_datetime_format": True}
                arguments = {**self.params}
                if hasattr(self, "pd_args") and isinstance(self.pd_args, dict):
                    arguments = {**self.params, **self.pd_args}
                try:
                    # can we use pyarrow.
                    engine = arguments["engine"]
                    del arguments["engine"]
                except KeyError:
                    engine = "c"
                tp = pd.read_csv(
                    self.filename,
                    sep=self.separator,
                    decimal=",",
                    engine=engine,
                    keep_default_na=False,
                    na_values=["TBD", "NULL", "null"],
                    na_filter=True,
                    skipinitialspace=True,
                    iterator=True,
                    chunksize=1000,
                    **arguments,
                )
                df = pd.concat(tp, ignore_index=True)
            # read filename from self.filename
            self._result = self.filename
        elif self.data is not None:
            # is already a dataframe:
            df = self.data
            self._result = self.data
        else:
            return False
        if df is None or df.empty:
            raise DataNotFound(f"Empty File or Data: {self.filename}")
        # adding stat from dataframe:
        pd.set_option("display.float_format", lambda x: "%.3f" % x)
        self.add_metric("COLUMNS", df.columns)
        self.add_metric("ROWS", len(df.index))
        # removing empty cols
        if hasattr(self, "drop_empty"):
            df.dropna(axis="columns", how="all", inplace=True)
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if hasattr(self, "trim"):
            cols = list(df.columns)
            for col in cols:
                df[col] = df[col].astype(str).str.strip()
        if self._debug:
            print(df)
            # print('COLS: >> ', df.columns)
        columns = df.columns
        cols = []
        replaced_columns = list(self.replace_names.keys())
        if hasattr(self, "pre_rename"):
            ### can rename columns PREVIOUS TO normalize
            for col in columns:
                datatype = df.dtypes[col]
                try:
                    t = dtypes[datatype]
                except KeyError:
                    t = str
                if col in self.pre_rename:
                    col = self.pre_rename[col]
                col = self.rename_repeated_col(col, cols)
                f = (col, t)
                cols.append(f)
        elif hasattr(self, "normalize_names"):
            # TODO: avoid SQL-reserved words like SELECT, WITH, etc.
            for col in columns:
                datatypes = str(df.dtypes[col])
                t = str
                tmp_col = col
                try:
                    t = dtypes[datatypes]
                    data = df[col].iloc[0]
                    if datatypes == "object":
                        # try to infer datatype:
                        if isinstance(data, str) and data != np.nan:
                            if data.isalpha():
                                t = str
                            else:
                                try:
                                    dt = dateparser.parse(
                                        str(data), settings={"TIMEZONE": "UTC"}
                                    )
                                    if isinstance(dt, datetime.datetime):
                                        t = datetime.datetime
                                except (ValueError, TypeError):
                                    pass
                except KeyError:
                    t = str

                if isinstance(col, (datetime.datetime, datetime.date)):
                    mask = getattr(self, "mask_datetime", "%b_%d_%Y")
                    new_name = datetime_to_name(col, mask)
                elif is_snakecase(col):
                    new_name = col.strip().lower()
                elif is_camelcase(col):
                    new_name = "_".join(
                        [x.lower().strip() for x in camelcase_split(col)]
                    )
                else:
                    new_name = re.sub(r"[^a-zA-Z0-9_]", "", col).strip()
                    if hasattr(self, "normalize"):
                        ## making some changes on col_name:
                        if (
                            "remove_prefix" in self.normalize and self.normalize["remove_prefix"]
                        ):
                            prefix = self.normalize["remove_prefix"]
                            new_name = new_name.removeprefix(prefix)
                        if "trim" in self.normalize and self.normalize["trim"] is True:
                            new_name = new_name.strip()
                        ### remove any illegal character
                        new_name = remove_illegal_chars(new_name)
                        # re-covert again from camelCase:
                        if (
                            "camelcase" in self.normalize and self.normalize["camelcase"] is True
                        ):
                            new_name = new_name.replace(" ", "").translate(
                                str.maketrans("", "", "/:.")
                            )
                            new_name = re.sub(r"\([^)]*\)", "", new_name)
                        else:
                            new_name = "_".join(
                                [x.lower().strip() for x in camelcase_split(new_name)]
                            )
                # RENAMING THE COLUMN WITH A NEW NAME:
                if new_name in replaced_columns:
                    replace = self.replace_names[new_name]
                    if isinstance(replace, str):
                        new_name = self.replace_names[new_name]
                    elif isinstance(replace, dict):
                        if "name" in replace:
                            new_name = replace["name"]
                        if "type" in replace:
                            t = dtypes[replace["type"]]
                    else:
                        # wrong arguments for Replace Names
                        pass
                if new_name in self.fields:
                    t = dtypes[self.fields[new_name]]
                new_name = self.rename_repeated_col(new_name, cols)
                f = (new_name, t)
                cols.append(f)
                if tmp_col == new_name:
                    self._logger.warning(
                        f"The Column '{new_name}' has not normalized"
                    )
                else:
                    self._logger.debug(
                        f" - Normalized Name: {new_name}"
                    )
        else:
            for col in columns:
                datatype = df.dtypes[col]
                try:
                    t = dtypes[datatype]
                except KeyError:
                    t = str
                col = self.rename_repeated_col(col, cols)
                f = (col, t)
                cols.append(f)
        try:
            cls = Model.make_model(name=self.tablename, schema=self.schema, fields=cols)
        except Exception as err:
            print("ERROR:", err)
            raise ComponentError(str(err)) from err
        if cls:
            mdl = cls()  # empty model, I only need the schema
            # TODO: open the metadata table and compare with model
            if sql := mdl.model(dialect="sql"):
                print("SQL IS ", sql)
                print('CREDENTIALS > ', self.credentials)
                if not self.credentials:
                    db = self.default_connection('pg')
                else:
                    db = self.get_connection(
                        params=self.credentials
                    )
                async with await db.connection() as conn:
                    if self.drop is True:
                        result, error = await conn.execute(
                            sentence=f"DROP TABLE IF EXISTS {self.schema}.{self.tablename};"
                        )
                        logging.debug(f"TableSchema: {result}, {error}")
                    result, error = await conn.execute(sentence=sql)
                    if error:
                        raise ComponentError(f"Error on Table creation: {error}")
                    else:
                        self.add_metric("Table", result)
                        if self._debug is True:
                            logging.debug(f"TableSchema: {result!s}")
                    # add Primary Key to table:
                    if hasattr(self, "pk"):
                        pk = pk_sentence.format(
                            schema=self.schema,
                            table=self.tablename,
                            fields=",".join(self.pk),
                        )
                        _primary, error = await conn.execute(sentence=pk)
                        logging.debug(f"TableSchema: PK creation: {_primary}, {error}")
        # passthrough the previous component value:
        self._result = self.input
        return self.input

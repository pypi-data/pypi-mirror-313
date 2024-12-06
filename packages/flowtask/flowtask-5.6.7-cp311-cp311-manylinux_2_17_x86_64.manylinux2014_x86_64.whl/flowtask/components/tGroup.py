import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class tGroup(FlowComponent):
    """
    tGroup

        Overview

            The tGroup class is a component for performing a group-by operation on a DataFrame using specified columns.
            It returns unique combinations of the specified group-by columns, allowing data aggregation and summarization.

        .. table:: Properties
        :widths: auto

            +----------------+----------+-----------+---------------------------------------------------------------+
            | Name           | Required | Summary                                                                   |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | group_by       |   Yes    | List of columns to group by.                                              |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | columns        |   No     | List of columns to retain in the result DataFrame. If None,               |
            |                |          | all columns in `group_by` are returned.                                   |
            +----------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component returns a DataFrame with unique rows based on the specified `group_by` columns. If `columns`
            is defined, only those columns are included in the result. The component provides debugging information on
            column data types if enabled, and any errors during grouping are logged and raised as exceptions.
    """ #noqa

    condition = ""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._columns: list = kwargs.pop("group_by", None)
        if not self._columns:
            raise ConfigError(
                "tGroup require a list of Columns for Group By => **group_by**"
            )
        super(tGroup, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", status=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe", status=404)
        return True

    async def close(self):
        pass

    async def run(self):
        self._result = None
        try:
            # Get unique region names
            df = self.data[self._columns].drop_duplicates().reset_index(drop=True)
        except Exception as err:
            raise ComponentError(f"Generic Error on Data: error: {err}") from err
        if hasattr(self, "columns"):
            # returning only a subset of data
            df = df[self.columns]
        if self._debug is True:
            print("::: Printing Column Information === ")
            print("Grouped: ", df)
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        self._result = df
        return True

import asyncio
from typing import Union
from collections.abc import Callable
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas

class tPivot(tPandas):
    """
        tPivot

        Overview

        Pivoting a Dataframe to transpose a column into other columns.

        Properties

        .. table:: Properties
        :widths: auto

        +------------------+----------+-----------+-----------------------------------------------------------------------------------+
        | Name             | Required | Type      | Description                                                                       |
        +------------------+----------+-----------+-----------------------------------------------------------------------------------+
        | columns          | Yes      | list      | The List of Columns to be Pivoted.                                                |
        +------------------+----------+-----------+-----------------------------------------------------------------------------------+
        | index            | No       | list      | List of columns to be preserved, default to all columns less "values"             |
        +------------------+----------+-----------+-----------------------------------------------------------------------------------+
        | values           | Yes      | str       | Columns that transpose the values for pivoted column(s).                          |
        +------------------+----------+-----------+-----------------------------------------------------------------------------------+

        Return
           The dataframe Pivoted by "columns" with values using the list of "values".

    """  # noqa
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._columns: Union[str, list] = kwargs.pop("columns", None)
        self._index: list = kwargs.pop("index", [])
        self._values: list = kwargs.pop("values", [])
        self._aggfunc: str = kwargs.pop('aggfunc', 'sum')
        self._sort: list = kwargs.pop('sort_by', [])
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def _run(self):
        try:
            df_pivot = self.data.pivot_table(
                index=self._index,
                columns=self._columns,
                values=self._values,
                aggfunc=self._aggfunc,
                dropna=False
            ).reset_index()
            # Renaming the columns to match the desired output
            df_pivot.columns.name = None  # Remove the index name
            if self._sort:
                df_pivot = df_pivot.sort_values(
                    by=self._sort,
                    ascending=True
                ).reset_index(drop=True)
            return df_pivot
        except Exception as err:
            raise ComponentError(
                f"Generic Error on Data: error: {err}"
            ) from err

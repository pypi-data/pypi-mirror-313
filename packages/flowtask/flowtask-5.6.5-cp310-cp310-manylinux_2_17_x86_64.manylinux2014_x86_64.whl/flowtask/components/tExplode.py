import asyncio
from typing import Any
from collections.abc import Callable
import pandas
from pandas import json_normalize
from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent


class tExplode(FlowComponent):
    """
    tExplode

        Overview

            The tExplode class is a component for transforming a DataFrame by converting a column of lists or dictionaries
            into multiple rows. It supports options for dropping the original column after exploding, and for expanding
            nested dictionary structures into separate columns.

        .. table:: Properties
        :widths: auto

            +----------------+----------+-----------+-------------------------------------------------------------------------------+
            | Name           | Required | Summary                                                                                   |
            +----------------+----------+-----------+-------------------------------------------------------------------------------+
            | column         |   Yes    | The name of the column to explode into multiple rows.                                     |
            +----------------+----------+-----------+-------------------------------------------------------------------------------+
            | drop_original  |   No     | Boolean indicating if the original column should be dropped after exploding.              |
            +----------------+----------+-----------+-------------------------------------------------------------------------------+
            | explode_dataset|   No     | Boolean specifying if nested dictionaries in the column should be expanded as new columns.|
            +----------------+----------+-----------+-------------------------------------------------------------------------------+

        Returns

            This component returns a DataFrame with the specified column exploded into multiple rows. If `explode_dataset` is
            set to True and the column contains dictionaries, these are expanded into new columns. Metrics on the row count
            after explosion are recorded, and any errors encountered during processing are logged and raised as exceptions.
    """ #noqa

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.data: Any = None
        # Column to be exploded
        self.column: str = kwargs.pop("column", None)
        self.drop_original: bool = kwargs.pop("drop_original", False)
        # Useful when exploded column is also composed of dictionary, the dictionary
        # is also exploded as columns
        self.explode_dataset: bool = kwargs.pop("explode_dataset", True)
        super(tExplode, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", status=404)
        if not isinstance(self.data, pandas.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe", status=404)
        return True

    async def run(self):
        args = {}
        if self.data.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 1")

        # Explode the Rows:
        try:
            # Step 1: Explode the 'field' column
            exploded_df = self.data.explode(self.column)
            # Reset index to ensure it's unique
            exploded_df = exploded_df.reset_index(drop=True)
            if self.explode_dataset is True:
                # Step 2: Normalize the JSON data in 'exploded' col
                # This will create a new DataFrame where each dictionary key becomes a column
                data_df = json_normalize(exploded_df[self.column])
                # Step 3: Concatenate with the original DataFrame
                # Drop the original column from exploded_df and join with data_df
                if self.drop_original is True:
                    exploded_df.drop(self.column, axis=1)
                df = pandas.concat([exploded_df, data_df], axis=1)
            else:
                df = exploded_df
        except Exception as err:
            raise ComponentError(f"Error Merging Dataframes: {err}") from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound("Concat: Cannot make any Explode")
        if hasattr(self, "index"):
            df[self.index] = df["id"]
            df.drop("id", axis="columns", inplace=True)
        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        self.add_metric("EXPLODE: ", numrows)
        df.is_copy = None
        print(df)
        self._result = df
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        return self._result

    async def close(self):
        pass

from typing import Union, Any, ParamSpec
import orjson
import pandas as pd
from .abstract import BaseDataframe
from ...exceptions import ComponentError, DataNotFound

P = ParamSpec("P")


def is_empty(obj):
    """check_empty.
    Check if a basic object is empty or not.
    """
    if isinstance(obj, pd.DataFrame):
        return True if obj.empty else False
    else:
        return bool(not obj)


class PandasDataframe(BaseDataframe):
    """PandasDataframe.

    Converts any result into a Pandas DataFrame.
    """
    async def create_dataframe(
        self,
        result: Union[dict, bytes, Any],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> Any:
        """
        Converts any result into a Pandas DataFrame.

        :param result: The result data to be converted into a Pandas DataFrame.
        :return: A DataFrame containing the result data.
        """
        if is_empty(result):
            raise DataNotFound("DataFrame: No Data was Found.")
        try:
            if isinstance(result, str):
                try:
                    result = orjson.loads(result)
                except Exception:
                    pass
            if isinstance(result, dict):
                result = [result]
            df = pd.DataFrame(result, **kwargs)
            # Attempt to infer better dtypes for object columns.
            df.infer_objects()
            columns = list(df.columns)
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes(convert_string=self.to_string)
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes()
            if hasattr(self, "drop_empty"):
                df.dropna(axis=1, how="all", inplace=True)
                df.dropna(axis=0, how="all", inplace=True)
            if hasattr(self, "dropna"):
                df.dropna(subset=self.dropna, how="all", inplace=True)
            numrows = len(df.index)
            try:
                self._variables["_numRows_"] = numrows
                self.add_metric("NUM_ROWS", numrows)
                self.add_metric("NUM_COLS", len(columns))
            except Exception:
                pass
            return df
        except Exception as err:
            raise ComponentError(
                f"Error Creating Dataframe: {err!s}"
            )

    async def from_csv(
        self, result: str, *args: P.args, **kwargs: P.kwargs
    ) -> Any:
        """
        Converts a Comma-Separated CSV into a Pandas DataFrame.

        :param result: The result data to be converted into a Pandas DataFrame.
        :return: A DataFrame containing the result data.
        """
        if is_empty(result):
            raise DataNotFound("DataFrame: No Data was Found.")
        try:
            df = pd.read_csv(result, encoding="utf-8", **kwargs)
            # Attempt to infer better dtypes for object columns.
            df.infer_objects()
            columns = list(df.columns)
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes(convert_string=self.to_string)
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes()
            if hasattr(self, "drop_empty"):
                df.dropna(axis=1, how="all", inplace=True)
                df.dropna(axis=0, how="all", inplace=True)
            if hasattr(self, "dropna"):
                df.dropna(subset=self.dropna, how="all", inplace=True)
            numrows = len(df.index)
            try:
                self._variables["_numRows_"] = numrows
                self.add_metric("NUM_ROWS", numrows)
                self.add_metric("NUM_COLS", len(columns))
            except Exception:
                pass
            return df
        except Exception as err:
            raise ComponentError(f"Error Creating Dataframe: {err!s}")

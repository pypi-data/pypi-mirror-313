from typing import Union, Any
import pandas as pd
from navconfig.logging import logging


def average(
    df: pd.DataFrame,
    desc: Any,
    column_name: str,
    threshold: Union[int, float],
    deviation: Union[int, float] = 2,
    allow_below: bool = False,
    allow_above: bool = False,
):
    """average.

    Args:
        df (pd.DataFrame): _description_
        desc (Any): _description_
        colname (str): _description_
        threshold (Union[int, float]): _description_
        deviation (Union[int, float]): _description_
    """
    value = desc.loc["mean", column_name]
    allowed_deviation = threshold * deviation / 100
    _min = threshold - allowed_deviation
    _max = threshold + allowed_deviation
    print("MIN ", _min, "MAX ", _max)
    val = bool(_min <= value <= _max)
    logging.debug(f"Current Average value: {value}")
    if value <= _min and allow_below is True:
        val = True
    if value >= _max and allow_above is True:
        val = True
    return value, val


def between(df: pd.DataFrame, desc: Any, column_name: str, values: tuple):
    """
    Check if the values in a DataFrame column are between the given min and max values.

    Args:
    - df (pd.DataFrame): The DataFrame to check.
    - desc (Any): The description (usually from df.describe()) of the DataFrame.
    - column_name (str): The name of the column to check.
    - values (tuple): A tuple containing the (min, max) values.

    """
    min_value = desc.loc["min", column_name]
    max_value = desc.loc["max", column_name]
    min_threshold, max_threshold = values
    val = min_threshold <= min_value and max_value <= max_threshold
    return (min_value, max_value), val


def equal(df: pd.DataFrame, desc: Any, column_name: str, values: tuple):
    """
    Check if all values in a DataFrame column are within the provided list of strings.

    Args:
    - df (pd.DataFrame): The DataFrame to check.
    - column_name (str): The name of the column to check.
    - values (tuple): A tuple containing the allowed strings.

    """
    return values, bool(df[column_name].isin(values).all())

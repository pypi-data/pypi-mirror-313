"""Functions for FilterRows."""
import re
import numpy as np


def drop_columns(dataframe, columns: list = [], endswith: list = [], startswith: list = []):
    """
    This function drops specified columns from a DataFrame based on exact names, suffixes, or prefixes.

    :param dataframe: The DataFrame from which columns will be dropped.
    :param columns: List of exact column names to drop.
    :param endswith: List of suffixes; columns ending with these will be dropped.
    :param startswith: List of prefixes; columns starting with these will be dropped.
    :return: The DataFrame with specified columns dropped.
    """
    if columns and isinstance(columns, list):
        dataframe.drop(axis=1, columns=columns, inplace=True, errors="ignore")
    elif endswith and isinstance(endswith, list):
        cols_to_drop = [col for col in dataframe.columns if col.endswith(tuple(endswith))]
        dataframe = dataframe.drop(columns=cols_to_drop)
    elif startswith and isinstance(startswith, list):
        cols_to_drop = [col for col in dataframe.columns if col.startswith(tuple(startswith))]
        dataframe = dataframe.drop(columns=cols_to_drop)
    return dataframe


def drop_rows(df, **kwargs):
    """
    This function drops rows from a DataFrame based on specified column values.

    :param df: The DataFrame from which rows will be dropped.
    :param kwargs: Column names and their corresponding values to drop rows.
    :return: The DataFrame with specified rows dropped.
    """
    for column, expression in kwargs.items():
        if isinstance(expression, list):
            mask = df[column].isin(expression)
            df = df[~mask]
            df.head()
    return df


def drop_duplicates(dataframe, columns=[], **kwargs):
    """
    This function drops duplicate rows from a DataFrame based on specified columns.

    :param dataframe: The DataFrame from which duplicates will be dropped.
    :param columns: List of columns to consider for identifying duplicates.
    :param kwargs: Additional keyword arguments for drop_duplicates method.
    :return: The DataFrame with duplicates dropped.
    """
    if columns and isinstance(columns, list):
        dataframe.set_index(columns, inplace=True, drop=False)
        dataframe.sort_values(by=columns, inplace=True)
        dataframe.drop_duplicates(subset=columns, inplace=True, **kwargs)
    return dataframe


def clean_empty(dataframe, columns=[]):
    """
    This function drops rows from a DataFrame where specified columns are empty, NaN, or contain empty strings.

    :param dataframe: The DataFrame from which rows will be dropped.
    :param columns: List of columns to check for empty values.
    :return: The DataFrame with specified rows dropped.
    """
    if columns and isinstance(columns, list):
        for column in columns:
            condition = dataframe[
                (dataframe[column].empty)
                | (dataframe[column] == "")
                | (dataframe[column].isna())
            ].index
            dataframe.drop(condition, inplace=True)
    return dataframe


def suppress(dataframe, columns=[], **kwargs):
    """
    This function suppresses parts of string values in specified columns based on a regex pattern.

    :param dataframe: The DataFrame containing the columns to be modified.
    :param columns: List of columns to apply the suppression.
    :param kwargs: Additional keyword arguments, including 'pattern' for the regex.
    :return: The DataFrame with suppressed string values.
    """
    if "pattern" in kwargs:
        pattern = kwargs["pattern"]

    def clean_chars(field):
        name = str(field)
        if re.search(pattern, name):
            pos = re.search(pattern, name).start()
            return str(name)[:pos]
        else:
            return name

    if columns and isinstance(columns, list):
        for column in columns:
            dataframe[column] = dataframe[column].astype(str)
            dataframe[column] = dataframe[column].apply(clean_chars)
    return dataframe


def fill_na(df, columns: list = [], fill_value="", **kwargs):
    """
    This function fills NaN values in specified columns with a given fill value.

    :param df: The DataFrame containing the columns to be filled.
    :param columns: List of columns to fill NaN values.
    :param fill_value: The value to replace NaN values with.
    :param kwargs: Additional keyword arguments.
    :return: The DataFrame with NaN values filled.
    """
    df[columns] = (
        df[columns].astype(str).replace(["nan", np.nan], fill_value, regex=True)
    )
    # self.data[u.columns].replace({pandas.NaT: None})
    return df

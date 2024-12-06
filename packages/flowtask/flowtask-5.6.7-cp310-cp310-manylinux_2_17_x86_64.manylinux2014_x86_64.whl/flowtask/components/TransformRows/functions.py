"""
Functions.

Tree of TransformRows functions.

"""
from typing import Optional
import requests
import pandas
from ...conf import BARCODELOOKUP_API_KEY
from ...utils.executor import getFunction


def apply_function(
    df: pandas.DataFrame,
    field: str,
    fname: str,
    column: Optional[str] = None,
    **kwargs
) -> pandas.DataFrame:
    """
    Apply any scalar function to a column in the DataFrame.

    Parameters:
    - df: pandas DataFrame
    - field: The column where the result will be stored.
    - fname: The name of the function to apply.
    - column: The column to which the function is applied (if None, apply to `field` column).
    - **kwargs: Additional arguments to pass to the function.
    """

    # Retrieve the scalar function using getFunc
    try:
        func = getFunction(fname)
    except Exception:
        raise

    # If a different column is specified, apply the function to it,
    # but save result in `field`
    try:
        if column is not None:
            df[field] = df[column].apply(lambda x: func(x, **kwargs))
        else:
            if field not in df.columns:
                # column doesn't exist
                df[field] = None
            # Apply the function to the field itself
            df[field] = df[field].apply(lambda x: func(x, **kwargs))
    except Exception as err:
        print(
            f"Error in apply_function for field {field}:", err
        )
    return df


def get_product(row, field, columns):
    """
    Retrieves product information from the Barcode Lookup API based on a barcode.

    :param row: The DataFrame row containing the barcode.
    :param field: The name of the field containing the barcode.
    :param columns: The list of columns to extract from the API response.
    :return: The DataFrame row with the product information.
    """

    barcode = row[field]
    url = f'https://api.barcodelookup.com/v3/products?barcode={barcode}&key={BARCODELOOKUP_API_KEY}'
    response = requests.get(url)
    result = response.json()['products'][0]
    for col in columns:
        try:
            row[col] = result[col]
        except KeyError:
            row[col] = None
    return row


def upc_to_product(
    df: pandas.DataFrame,
    field: str,
    columns: list = ['barcode_formats', 'mpn', 'asin', 'title', 'category', 'model', 'brand']
) -> pandas.DataFrame:
    """
    Converts UPC codes in a DataFrame to product information using the Barcode Lookup API.

    :param df: The DataFrame containing the UPC codes.
    :param field: The name of the field containing the UPC codes.
    :param columns: The list of columns to extract from the API response.
    :return: The DataFrame with the product information.
    """
    try:
        df = df.apply(lambda x: get_product(x, field, columns), axis=1)
        return df
    except Exception as err:
        print(f"Error on upc_to_product {field}:", err)
        return df

from typing import Union, Tuple


def average(
    data: dict,
    column: str,
    threshold: Union[int, float],
    deviation: Union[int, float],
    allow_below: bool = False,
):
    """average.

    Calculates the average of a value compared with a threshold.
    Args:
        data (dict): extract column from data.
        column (str): column to calculate.
        threshold (float): value to be used for threshold
        deviation (float): max deviation acceptable for threshold
        allow_below (bool): if True, the threshold is not evaluated on minimum values.
    """
    value = data.get(column, None)
    allowed_deviation = threshold * deviation / 100
    _min = threshold - allowed_deviation
    _max = threshold + allowed_deviation
    print("MIN ", _min, "MAX ", _max)
    val = _min <= value <= _max
    if value <= _min and allow_below is True:
        val = True
    return column, value, val


def max_value(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Checks if the actual value of a specified column in the data is less than or equal to the
    given threshold value.

    Args:
        data (dict): Dictionary containing the data to be checked.
        column (str): Name of the column in the data whose value needs to be checked.
        value (Union[int, float]): The threshold value. The actual value in the data
          should be less than or equal to this.

    Returns:
        tuple: A tuple containing:
            - column (str): Name of the column that was checked.
            - actual_value (Union[int, float]): The actual value from the data for the specified column.
            - val (bool): True if the actual value is less than or equal to the threshold, False otherwise.
    """
    actual_value = data.get(column, None)
    val = actual_value <= value
    return column, actual_value, val


def min_value(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Checks if the actual value of a specified column in the data is greater than or
    equal to the given threshold value.

    Args:
        data (dict): Dictionary containing the data to be checked.
        column (str): Name of the column in the data whose value needs to be checked.
        value (Union[int, float]): The threshold value. The actual value in the data
          should be greater than or equal to this.

    Returns:
        tuple: A tuple containing:
            - column (str): Name of the column that was checked.
            - actual_value (Union[int, float]): The actual value from the data for the specified column.
            - val (bool): True if the actual value is greater than or equal
              to the threshold, False otherwise.
    """
    actual_value = data.get(column, None)
    val = actual_value >= value
    return column, actual_value, val

from __future__ import annotations
from datetime import datetime

try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None

def convert_to_list(arg):
    """Converts various data types to a Python list format.

    Args:
        arg: The input object to be converted to a list.

    Returns:
        A Python list containing the converted values from the input.
    """
    try:
        if arg is None:
            return None
        elif isinstance(arg, list):
            return arg
        elif isinstance(arg, (int, float, str)):
            return [arg]
        elif isinstance(arg, (tuple, set)):
            return list(arg)
        elif isinstance(arg, dict):
            return list(arg.values())
        elif np and isinstance(arg, np.ndarray):
            return arg.tolist()
        elif pd and isinstance(arg, (pd.Series, pd.Index)):
            return arg.tolist()
        return list(arg)
    except TypeError:
        raise TypeError(f'Data type {type(arg)} is not supported.')

def convert_to_dict(arg):
    """Converts various data types to a Python dictionary format.

    Args:
        arg: The input object to be converted to a dictionary.

    Returns:
        A Python dictionary containing the converted values from the input.
    """
    try:
        if arg is None:
            return None
        elif isinstance(arg, list):
            for i in range(len(arg)):
                arg[i] = convert_to_dict(arg[i])
            return arg
        elif isinstance(arg, dict):
            return arg
        elif pd and isinstance(arg, pd.DataFrame):
            return arg.to_dict(orient='records')
        elif pd and isinstance(arg, pd.Series):
            return arg.to_dict()
        return dict(arg)
    except TypeError:
        raise TypeError(f'Data type {type(arg)} is not supported.')

def convert_to_matrix(arg):
    """Converts various multidimensional data types to a Python matrix represented as
    a list of lists containing native Python numbers (int or float).

    Args:
        arg: The input object to be converted to a matrix.

    Returns:
        A Python list of lists representing the converted matrix.
    """
    try:
        if arg is None:
            return None
        elif isinstance(arg, list) and all(isinstance(row, list) for row in arg):
            return arg
        elif np and isinstance(arg, np.ndarray):
            return arg.tolist()
        elif pd and isinstance(arg, pd.DataFrame):
            return arg.values.tolist()
        elif isinstance(arg, tuple) and all(isinstance(row, (tuple, list)) for row in arg):
            return [list(row) for row in arg]
        elif hasattr(arg, '__iter__'):
            return [convert_to_matrix(item) for item in arg]
        return [arg]
    except TypeError:
        raise TypeError(f'Data type {type(arg)} is not supported.')

def convert_to_unix_time(arg, str_format: str = None):
    """Convert various datetime formats to Unix timestamp in milliseconds.

    Args:
        arg: The datetime value(s) to convert. Acceptable types include:
            int, float, datetime, pd.Timestamp, np.datetime64, str, or list
        str_format: The expected format of the string date if `arg` is a string and not in ISO format.
            This should follow the Python `datetime.strptime` format codes.

    Returns:
        A Unix timestamp in milliseconds as an integer if a single item was passed, or a list of
        Unix timestamps in milliseconds if a list was passed.
    """
    try:
        if isinstance(arg, list):
            for i in range(len(arg)):
                arg[i] = convert_to_unix_time(arg[i])
            return arg
        if isinstance(arg, (int, float)):
            return arg
        elif isinstance(arg, datetime):
            return int(arg.timestamp() * 1000)
        elif isinstance(arg, pd.Timestamp):
            return int(arg.timestamp() * 1000)
        elif isinstance(arg, np.datetime64):
            return int(arg.astype('datetime64[ms]').astype('int64'))
        elif isinstance(arg, str):
            if str_format:
                return int(datetime.strptime(arg, str_format).timestamp() * 1000)
            else:
                return int(datetime.fromisoformat(arg).timestamp() * 1000)
    except ValueError:
        raise ValueError("Input cannot be converted to a timestamp")


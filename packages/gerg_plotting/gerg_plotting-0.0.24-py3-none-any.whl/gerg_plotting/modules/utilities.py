# utilities.py

import numpy as np
import pandas as pd
import datetime


def to_numpy_array(values) -> np.ndarray:
    # convert set to list for pandas can convert to numpy array

    # Early return if values is None
    if values is None:
        return None
    # Return early if values are already a numpy array
    elif isinstance(values, np.ndarray):
        return values
    if isinstance(values,dict):
        raise TypeError(f"Cannot convert a dict with values of '{values}' to a NumPy array")
    # Convert set to list before attempting to convert
    elif isinstance(values,set):
        values = list(values)
    # Try to convert to numpy using pandas series as the parser
    array = pd.Series(values).to_numpy()
    return array


def calculate_range(var) -> list[float,float]:
    return [np.nanmin(var), np.nanmax(var)]


def calculate_pad(var, pad=0.0) -> tuple[float,float]:
    start, stop = calculate_range(var)
    start_with_pad = start - pad
    stop_with_pad = stop + pad
    return float(start_with_pad), float(stop_with_pad)


def extract_kwargs(kwargs:dict, defaults:dict):
    """
    Extracts values from kwargs with defaults for missing keys.

    Parameters:
    -----------
    kwargs : dict
        The keyword arguments dictionary.
    defaults : dict
        A dictionary of default values for keys.

    Returns:
    --------
    dict
        A dictionary containing the extracted values.
    """
    return {key: kwargs.pop(key, default) for key, default in defaults.items()}

def extract_kwargs_with_aliases(kwargs, defaults):
    """
    Extracts values from kwargs, handling key aliases and defaults.

    Parameters:
    -----------
    kwargs : dict
        The keyword arguments dictionary.
    defaults : dict
        A dictionary where keys are the primary keys or tuples of aliases,
        and values are the default values.

    Returns:
    --------
    dict
        A dictionary containing the extracted values using the primary keys.
    """
    extracted = {}
    for keys, default in defaults.items():
        if not isinstance(keys, tuple):
            keys = (keys,)  # Ensure single keys are treated as tuples
        for key in keys:
            if key in kwargs:
                extracted[keys[0]] = kwargs.pop(key)
                break
        else:
            extracted[keys[0]] = default
    return extracted


def print_time(message) -> None:
    """
    Prints a message with the current time in 'HH:MM:SS' format.

    Parameters:
        message (str): The message to include in the output.
    """
    print(f"{message}: {datetime.datetime.today().strftime('%H:%M:%S')}")


def print_datetime(message) -> None:
    """
    Prints a message with the current date and time in 'YYYY-MM-DD HH:MM:SS' format.

    Parameters:
        message (str): The message to include in the output.
    """
    print(f"{message}: {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")

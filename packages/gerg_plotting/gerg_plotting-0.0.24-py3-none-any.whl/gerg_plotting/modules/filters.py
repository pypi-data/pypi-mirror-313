# filters.py

import numpy as np
import pandas as pd
import xarray as xr


def filter_var(var, min_value, max_value) -> np.ndarray:
    """
    Filters values in an iterable or array-like object based on a range.

    Parameters:
        var (iterable): Input data (e.g., numpy array, pandas Series, xarray DataArray, list).
        min_value (float): Minimum threshold (inclusive).
        max_value (float): Maximum threshold (inclusive).

    Returns:
        Same type as input `var`, with values outside the range replaced by NaN
    """
    if isinstance(var, xr.DataArray):
        var = var.where(var >= min_value)
        var = var.where(var <= max_value)
    elif isinstance(var, (np.ndarray, pd.Series)):
        if isinstance(var, pd.Series):
            series = True
        else:
            series = False
        var = np.where((var >= min_value) & (var <= max_value), var, np.nan)
        if series:
            var = pd.Series(var)
    elif isinstance(var, list):
        # Remove elements outside the range for lists
        var = [v if min_value <= v <= max_value else np.nan for v in var]
    else:
        raise TypeError("Unsupported data type. Must be xarray.DataArray, numpy array, pandas Series, or list.")
    return var


def filter_nan(values) -> np.ndarray:
    """
    Removes NaN values from an iterable or array-like object.

    Parameters:
        values (iterable): Input data (e.g., numpy array, pandas Series, xarray DataArray, list).

    Returns:
        Same type as input `values` with NaN values removed.
    """
    if isinstance(values, xr.DataArray):
        return values.dropna(dim="dim_0")  # Drops NaN along the first dimension
    elif isinstance(values, pd.Series):
        return values.dropna()
    elif isinstance(values, np.ndarray):
        return values[~np.isnan(values)]
    elif isinstance(values, list):
        return [v for v in values if not (v is None or np.isnan(v))]
    else:
        raise TypeError("Unsupported data type. Must be xarray.DataArray, numpy array, pandas Series, or list.")


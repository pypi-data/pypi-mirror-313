import numpy as np


def lat_min_smaller_than_max(instance, attribute, value) -> None:
    if value is not None:
        if value >= instance.lat_max:
            raise ValueError("'lat_min' must be smaller than 'lat_max'")


def lon_min_smaller_than_max(instance, attribute, value) -> None:
    if value is not None:
        if value >= instance.lon_max:
            raise ValueError("'lon_min' must be smaller than 'lon_max'")


def is_flat_numpy_array(instance, attribute, value) -> None:
    if not isinstance(value, np.ndarray):
        raise ValueError(f"{attribute.name} must be a NumPy array or a list convertible to a NumPy array")
    if value.ndim != 1:
        raise ValueError(f"{attribute.name} must be a flat array")
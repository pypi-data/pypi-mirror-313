import numpy as np
import pandas as pd
import xarray as xr
from itertools import combinations
import re

from gerg_plotting.data_classes.Data import Data


def normalize_string(input_string: str) -> str:
    """
    Normalizes a string by performing the following actions:
    - Converts the string to lowercase.
    - Replaces spaces, newlines, and other specified characters with underscores.
    - Removes leading and trailing underscores.
    - Collapses multiple consecutive underscores into a single underscore.

    Parameters:
    input_string (str): The string to normalize.

    Returns:
    str: The normalized string.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")
    
    # Define the characters to be replaced by underscores
    replace_pattern = r"[ \t\n\r\f\v.,;:!@#$%^&*()+=?/<>|\\\"'`~\[\]{}]"
    
    # Convert to lowercase
    normalized = input_string.lower()
    
    # Replace specified characters with underscores
    normalized = re.sub(replace_pattern, "_", normalized)
    
    # Collapse multiple underscores into one
    normalized = re.sub(r"__+", "_", normalized)
    
    # Remove leading and trailing underscores
    normalized = normalized.strip("_")
    
    return normalized


def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def create_combinations_with_underscore(strings):
    """
    Generate all pairwise combinations of strings with an underscore.

    Args:
        strings (list): A list of strings.

    Returns:
        list: A list of combinations joined by an underscore.
    """
    # Generate all pairwise combinations
    pairs = combinations(strings, 2)
    # Join each pair with an underscore
    combination= ["_".join(pair) for pair in pairs]
    combination.extend(strings)
    return combination

def custom_legend_handles(labels:list[str],colors,hatches=None,color_hatch_not_background:bool=False):
    '''
    Create Legend handles from the provided lables and colors
    '''
    import matplotlib.patches as mpatches

    assert len(labels) == len(colors)

    labels = [label.replace('_','/') for label in labels]

    if hatches is None:
        hatches = [None for _ in labels]

    if color_hatch_not_background:
        legend_handles = [mpatches.Patch(edgecolor=color, facecolor='none', label=label, hatch=hatch) for color, label, hatch in zip(colors, labels, hatches)]

    else:
        # Create custom legend handles
        legend_handles = [mpatches.Patch(facecolor=color, label=label, hatch=hatch) for color, label, hatch in zip(colors, labels, hatches)]

    return legend_handles

def _map_variables(keys:list[str], values:list[str], synonyms:dict[str,list[str]]|None=None, blocklist:dict[str,list[str]]|None=None):
    """
    Maps each key from the keys list to the most likely corresponding value from the values list,
    using optional synonyms and blocklist terms for flexible and precise matching.
    
    Parameters:
    - keys (list): List of keys to be used in the dictionary.
    - values (list): List of possible values to map to keys.
    - synonyms (dict, optional): Dictionary where each key has a list of synonyms to assist in matching.
    - blocklist (dict, optional): Dictionary where each key has a list of words to avoid for that key.
    
    Returns:
    - dict: Dictionary mapping each key to a corresponding value or None if no match is found.
    """
    # Initialize the dictionary with None for each key
    mapped_dict = {key: None for key in keys}
    
    # Iterate through each key
    for key in keys:
        # Gather possible matches, starting with the key itself
        possible_matches = [key]
        
        # Add synonyms if provided
        if synonyms and key in synonyms:
            possible_matches.extend(synonyms[key])
        
        # Get blocked words for the key if provided
        blocked_words = blocklist.get(key, []) if blocklist else []
        
        # Search through values for matches
        for value in values:
            # Check if the value is blocked for the key
            if any(block.lower() in value.lower() for block in blocked_words):
                continue  # Skip this value since it's blocked

            # Check for exact matches
            if any(match.lower() == value.lower() for match in possible_matches):
                mapped_dict[key] = value
                break
            
            # Check if this is a single-letter key (like 'u', 'v', 'w', or 's')
            if len(key) == 1:
                # Check the synonyms first
                if any(match.lower() == value.lower() for match in possible_matches):
                    mapped_dict[key] = value
                    break
                # Ensure the key appears only at the start or end of the value string
                elif value.lower().startswith(key.lower()) or value.lower().endswith(key.lower()):
                    mapped_dict[key] = value
                    break
            else:
                # Check for matching using synonyms and the key itself
                if any(match.lower() in value.lower() for match in possible_matches):
                    mapped_dict[key] = value
                    break
    
    return mapped_dict



def _get_var_mapping(df:pd.DataFrame) -> dict:
    keys = ['lat', 'lon', 'depth', 'time', 'temperature', 'salinity', 'density', 'u', 'v','w', 'speed']
    values = df.columns.tolist()
    synonyms = {
        'depth': ['pressure', 'pres'],
        'temperature': ['temp', 'temperature_measure'],
        'salinity': ['salt', 'salinity_level'],
        'density': ['density_metric', 'rho'],
        'u': ['eastward_velocity', 'u_component', 'u_current', 'current_u'],
        'v': ['northward_velocity', 'v_component', 'v_current', 'current_v'],
        'w': ['downward_velocity','upward_velocity','w_component', 'w_current', 'current_w'],
        's': ['combined_velocity','velocity','speed', 's_current', 'current_s']
    }
    blocklist = {
        's': ['sound','pres']
    }

    mapped_variables = _map_variables(keys, values, synonyms, blocklist)

    return mapped_variables


def interp_glider_lat_lon(ds:xr.Dataset) -> xr.Dataset:
    # Convert time and m_time to float64 for interpolation
    new_time_values = ds['time'].values.astype('datetime64[ns]').astype('float64')
    new_mtime_values = ds['m_time'].values.astype('datetime64[ns]').astype('float64')

    # Create masks of non-NaN values for both latitude and longitude
    valid_latitude = ~np.isnan(ds['latitude'])
    valid_longitude = ~np.isnan(ds['longitude'])

    # Interpolate latitude based on valid latitude and m_time values
    ds['latitude'] = xr.DataArray(
        np.interp(new_time_values, new_mtime_values[valid_latitude], ds['latitude'].values[valid_latitude]),
        [('time', ds['time'].values)]
    )

    # Interpolate longitude based on valid longitude and m_time values
    ds['longitude'] = xr.DataArray(
        np.interp(new_time_values, new_mtime_values[valid_longitude], ds['longitude'].values[valid_longitude]),
        [('time', ds['time'].values)]
    )

    ds = ds.drop_vars('m_time')

    return ds


def data_from_df(df:pd.DataFrame,mapped_variables:dict|None=None,**kwargs):

    # If the user does not pass mapped_variables
    if mapped_variables is None:
        mapped_variables = _get_var_mapping(df)

    mapped_variables = {key:df[value] for key,value in mapped_variables.items() if value is not None}

    data = Data(**mapped_variables,**kwargs)

    return data


def data_from_csv(filename:str,mapped_variables:dict|None=None,**kwargs):

    df = pd.read_csv(filename)

    data = data_from_df(df,mapped_variables=mapped_variables,**kwargs)

    return data

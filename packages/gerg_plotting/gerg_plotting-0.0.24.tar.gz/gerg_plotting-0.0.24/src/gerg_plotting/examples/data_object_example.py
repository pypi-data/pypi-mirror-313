from gerg_plotting import Data, Variable, data_from_csv,data_from_df
import pandas as pd
import cmocean


def read_example_data(filepath):
    """Reads example data from a CSV file and returns a DataFrame."""
    return pd.read_csv(filepath, parse_dates=['time'])


def create_data_from_csv(filename):
    return data_from_csv(filename)


def create_data_from_df(df):
    return data_from_df(df)


def create_data_with_iterables(df):
    """
    Creates a Data object using iterable inputs (pandas.Series or numpy arrays).
    """
    data = Data(
        lat=df['latitude'], lon=df['longitude'], depth=df['pressure'], time=df['time'],
        salinity=df['salinity'], temperature=df['temperature'], density=df['density']
    )
    return data


def create_variable_objects(df):
    """
    Creates Variable objects for latitude, longitude, depth, time, temperature,
    salinity, and density using data from a DataFrame.
    """
    lat_var = Variable(data=df['latitude'], name='lat', cmap=cmocean.cm.haline, units='°N')
    lon_var = Variable(data=df['longitude'], name='lon', cmap=cmocean.cm.thermal, units='°W')
    depth_var = Variable(data=df['pressure'], name='depth', cmap=cmocean.cm.deep, units='m')
    time_var = Variable(data=df['time'], name='time', cmap=cmocean.cm.thermal)
    temperature_var = Variable(data=df['temperature'], name='temperature', cmap=cmocean.cm.thermal, units='°C', vmin=-10, vmax=40)
    salinity_var = Variable(data=df['salinity'], name='salinity', cmap=cmocean.cm.haline, vmin=28, vmax=40)
    density_var = Variable(data=df['density'], name='density', cmap=cmocean.cm.dense, units="kg/m\u00B3", vmin=1020, vmax=1035)

    return lat_var, lon_var, depth_var, time_var, temperature_var, salinity_var, density_var


def create_data_with_variables(lat_var, lon_var, depth_var, time_var, temperature_var, salinity_var, density_var):
    """
    Creates a Data object using Variable objects for each data variable.
    """
    data = Data(
        lat=lat_var, lon=lon_var, depth=depth_var, time=time_var,
        temperature=temperature_var, salinity=salinity_var, density=density_var
    )
    return data


def modify_data_attributes(data):
    """
    Demonstrates modifying attributes of variables in a Data object.
    """
    data['lat'].vmin = 27
    data['depth'].units = 'km'
    return data


def add_custom_variable(data, df, var_name):
    """
    Adds a custom variable to a Data object using data from a DataFrame.
    """
    custom_var = Variable(data=df[var_name], name=var_name, cmap=cmocean.cm.thermal, units='m/s', label='Speed of Sound (m/s)')
    data.add_custom_variable(custom_var)
    return data

def make_example_plot(data,var):
    from gerg_plotting.plotting_classes.Histogram import Histogram
    hist = Histogram(data)
    hist.plot(var)
    hist.save('example_plots/data_object_example.png')

def data_object_example():
    # Read the data
    filepath = 'example_data/sample_glider_data.csv'
    df = read_example_data(filepath)

    # Create Data object from a csv
    data_obj_from_csv = create_data_from_csv(filepath)
    print("Data object created from csv:", data_obj_from_csv)

    # Create Data object from a dataframe
    data_obj_from_df = create_data_from_df(df)
    print("Data object created from dataframe:", data_obj_from_df)

    # Create Data object using iterables
    data_iterables = create_data_with_iterables(df)
    print("Data object created with iterables:", data_iterables)

    # Create Variable objects
    lat_var, lon_var, depth_var, time_var, temperature_var, salinity_var, density_var = create_variable_objects(df)

    # Create Data object using Variable objects
    data_variables = create_data_with_variables(lat_var, lon_var, depth_var, time_var, temperature_var, salinity_var, density_var)
    print("Data object created with Variable objects:", data_variables)

    # Modify data attributes
    modified_data = modify_data_attributes(data_variables)
    print("Modified Data object:", modified_data)

    # Add a custom variable
    updated_data = add_custom_variable(modified_data, df, 'Turner_angle')
    print("Data object with custom variable added:", updated_data)

    # Create example plot to show custom variable
    make_example_plot(updated_data,'Turner_angle')


if __name__ == "__main__":
    data_object_example()

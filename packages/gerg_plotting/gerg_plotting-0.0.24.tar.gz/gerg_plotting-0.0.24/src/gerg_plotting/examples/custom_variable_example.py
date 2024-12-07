from gerg_plotting import Histogram,Variable,data_from_df
from gerg_plotting.modules.plotting import get_turner_cmap
import pandas as pd
from pathlib import Path


def custom_variable_example():
    # Let's read in the example data
    df = pd.read_csv('example_data/sample_glider_data.csv')

    # Let's initilize the data object
    data = data_from_df(df)

    cmap = get_turner_cmap()

    # Init Turner_angle Variable object
    Turner_angle = Variable(data=df['Turner_angle'],name='Turner_angle',cmap=cmap,units='m/s',vmin=-90,vmax=90)
    # Add the Turner_angle Variable object to the Data object
    data.add_custom_variable(Turner_angle)
    # Test by plotting a histogram
    hist = Histogram(data)
    hist.plot(var='Turner_angle')
    hist.save('example_plots/custom_variable_example.png')


if __name__ == "__main__":
    custom_variable_example()
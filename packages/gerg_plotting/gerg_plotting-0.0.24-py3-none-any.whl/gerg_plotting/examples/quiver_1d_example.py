from gerg_plotting import ScatterPlot,data_from_df
import pandas as pd

def quiver_1d_example():
    # Let's read in the example data
    df = pd.read_csv('example_data/sample_tabs_data.csv')
    # Group by the depth
    groups = [group for _,group in df.groupby('bin_depth')]
    # Init data from the first group
    data = data_from_df(groups[0])

    scatter = ScatterPlot(data)
    scatter.quiver1d(x='time',quiver_scale=700)
    scatter.save('example_plots/quiver_1d_example.png')


if __name__ == "__main__":
    quiver_1d_example()
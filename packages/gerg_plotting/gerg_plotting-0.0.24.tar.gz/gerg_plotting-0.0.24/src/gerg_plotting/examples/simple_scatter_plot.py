from gerg_plotting import ScatterPlot,data_from_csv


def simple_scatter_plot():
    # Let's read in the example data
    data = data_from_csv('example_data/sample_glider_data.csv')

    scatter = ScatterPlot(data)
    scatter.scatter('time','temperature')
    scatter.save('example_plots/simple_scatter_plot.png')

if __name__ == "__main__":
    simple_scatter_plot()
from gerg_plotting import data_from_csv,ScatterPlot


def simple_hovmoller_example():
    # Let's read in some example data
    data = data_from_csv('example_data/sample_glider_data.csv')

    scatter = ScatterPlot(data)

    scatter.hovmoller('temperature')

    scatter.save('example_plots/simple_hovmoller_example.png',dpi=300)

if __name__ == "__main__":
    simple_hovmoller_example()
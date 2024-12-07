from gerg_plotting.plotting_classes.ScatterPlot import ScatterPlot
from gerg_plotting.tools import data_from_csv


def tricontourf_example():
    data = data_from_csv('example_data/sample_glider_data.csv')

    plotter = ScatterPlot(data=data)

    plotter.tricontourf(x='time',y='depth',z='temperature')
    plotter.ax.invert_yaxis()

    plotter.save('example_plots/tricontourf_example.png')

if __name__ == "__main__":
    tricontourf_example()

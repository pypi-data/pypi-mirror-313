from gerg_plotting import data_from_csv,ScatterPlot
import matplotlib.pyplot as plt


def quiver_2d_example():
    data = data_from_csv('example_data/sample_tabs_data.csv')

    data.calculate_speed()

    data.speed.units = 'cm/s'

    scatter = ScatterPlot(data)
    scatter.quiver2d(x='time',y='depth',quiver_scale=800)
    scatter.ax.invert_yaxis()
    scatter.save('example_plots/quiver_2d_example.png')
    # If you want to show the plot
    # scatter.show()

if __name__ == "__main__":
    quiver_2d_example()
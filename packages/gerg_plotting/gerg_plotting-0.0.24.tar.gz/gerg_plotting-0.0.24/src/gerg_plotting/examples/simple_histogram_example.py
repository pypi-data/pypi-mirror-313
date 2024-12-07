from gerg_plotting import Data,Histogram
import numpy as np


def simple_histogram_example():
    # If you just want to look at the histogram:
    data = Data(temperature=np.random.normal(28,size=1000))

    Histogram(data).plot(var='temperature')

    # If you want to save the histogram figure:
    data = Data(temperature=np.random.normal(28,size=1000))

    hist = Histogram(data)  # Assign the histogram plotter to a variable
    hist.plot(var='temperature')

    hist.fig.savefig('example_plots/simple_histogram_example.png')  # Get the fig attribute from hist then the savefig method to save it


if __name__ == "__main__":
    simple_histogram_example()
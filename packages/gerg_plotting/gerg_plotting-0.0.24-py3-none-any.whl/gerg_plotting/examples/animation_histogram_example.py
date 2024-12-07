from gerg_plotting import Data,Histogram,Animator,cmocean
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def animation_histogram_example():
    # Let's make some example data
    n_points = 10000
    data = Data(temperature=np.random.normal(28,size=n_points))

    # Let's create a histogram function to plot the data how we would like
    def make_hists(sample,color,data=data):
        '''Plot Histogram based on sample size and color'''
        data_sample = data[:10*sample+1]  # Slice data
        hist = Histogram(data_sample)  # Init histogram plotter
        hist.plot('temperature',color=color,bins=30,range=(25,31))  # Plot 1-d histogram
        hist.ax.set_ybound(upper=80)  # Set the ybounds maximum to 80 for a clearer plot
        return hist.fig

    samples = np.arange(90)
    cmap = plt.get_cmap('Greens')
    cmap = cmocean.tools.crop_by_percent(cmap,30,which='both')
    colors = [cmap((idx*2)+10) for idx in samples]

    gif_filename = Path(__file__).parent.joinpath('example_plots/animation_histogram_example.gif')
    Animator().animate(plotting_function=make_hists,param_dict={'sample':samples,'color':colors},fps=12,gif_filename=gif_filename)


if __name__ == "__main__":
    animation_histogram_example()

from gerg_plotting import ScatterPlot,data_from_df
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def power_spectra_example():
    # Let's read in the example data
    df = pd.read_csv('example_data/sample_tabs_data.csv')

    # Init some base parameters
    samp_freq = 48
    seg_len = 256
    theta_rad = np.deg2rad(55)
    highlight_freqs = [1/10, 1, 2]
    y_limits = (10,10e5)

    # In this first example we will let the power_spectra_density function calculate the PSD for us,
    # we just need to supply a few parameters to the calculation

    # Init data
    data = data_from_df(df)
    # Init ScatterPlot
    scatter = ScatterPlot(data)
    # Plot power spectra density
    scatter.power_spectra_density(var_name='u',sampling_freq=samp_freq,segment_length=seg_len,theta_rad=theta_rad,
                                    highlight_freqs=highlight_freqs)
    # Set the ylimits so the plots all match up
    scatter.ax.set_ylim(*y_limits)
    # Add an informative title
    scatter.ax.set_title('Vector U')
    # scatter.show()


    # Now Let's look at a more advanced use

    # Import the Animator class
    from gerg_plotting import Animator

    # first we need to create a function that will return the figure
    def power_spectra_plot(group:pd.DataFrame):
        '''
        Plot the power spectra of vectors u, v, and w
        '''
        data = data_from_df(group)

        # We can calcluate the PSD using the calcluate_PSD method in the Data object
        psd_freq,psd_u,psd_v,psd_w = data.calcluate_PSD(sampling_freq=samp_freq,segment_length=seg_len,theta_rad=theta_rad)
        
        # Init the subplots
        fig,axes = plt.subplots(nrows=3,figsize=(10,18),layout='constrained')

        # Init the ScatterPlot
        scatter = ScatterPlot(data)
        # Plot the PSD for each vector and set their ylimits
        scatter.power_spectra_density(psd_freq=psd_freq,psd=psd_u,highlight_freqs=highlight_freqs,fig=fig,ax=axes[0])
        scatter.ax.set_title('Vector U')
        scatter.ax.set_ylim(*y_limits)
        scatter.power_spectra_density(psd_freq=psd_freq,psd=psd_v,highlight_freqs=highlight_freqs,fig=fig,ax=axes[1])
        scatter.ax.set_title('Vector V')
        scatter.ax.set_ylim(*y_limits)
        scatter.power_spectra_density(psd_freq=psd_freq,psd=psd_w,highlight_freqs=highlight_freqs,fig=fig,ax=axes[2])
        scatter.ax.set_title('Vector W')
        scatter.ax.set_ylim(*y_limits)
        # Add informative figure title
        scatter.fig.suptitle(f'Auto-spectra at Bin Depth: {group['bin_depth'].min()} m',fontsize=22)
        return scatter.fig

    # Extract groups by bin_depth
    groups = [group for _,group in df.groupby('bin_depth')]

    # Create an animation of the power spectra along depth
    Animator().animate(plotting_function=power_spectra_plot,param_dict={'group':groups},gif_filename='example_plots/power_spectra_example.gif',fps=0.75)

if __name__ == "__main__":
    power_spectra_example()
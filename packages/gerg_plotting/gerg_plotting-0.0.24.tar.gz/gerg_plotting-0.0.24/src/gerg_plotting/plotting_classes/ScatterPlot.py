import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import numpy as np
from attrs import define, field
import cmocean

from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.modules.calculations import get_sigma_theta, get_density
from gerg_plotting.data_classes.Variable import Variable

@define
class ScatterPlot(Plotter):
    """
    ScatterPlot class for creating various scatter plots from a SpatialInstrument's data.

    Inherits from the Plotter class to leverage figure, axis, and colorbar management functionalities.
    This class specifically deals with scatter plots that visualize relationships between different variables
    (e.g., temperature vs salinity, time vs depth) in the provided instrument data.
    
    Attributes:
        markersize (int | float): The size of the scatter plot markers.
    """
    
    markersize: int | float = field(default=10)

    def scatter(self, x: str, y: str, color_var: str | None = None, invert_yaxis:bool=False, fig=None, ax=None, **kwargs) -> None:
        """
        Create a scatter plot of two variables `x` and `y`, with optional coloring by a third variable.
        
        Args:
            x (str): The variable to plot on the x-axis.
            y (str): The variable to plot on the y-axis.
            color_var (str | None, optional): The variable to map to color (default is None).
            fig (matplotlib.figure.Figure, optional): The figure to use.
            ax (matplotlib.axes.Axes, optional): The axes to use.
        
        This method creates a scatter plot of the variables `x` and `y`, with optional coloring by `color_var`.
        """
        self.data.check_for_vars([x,y,color_var])
        self.init_figure(fig, ax)  # Initialize figure and axes

        # If color_var is passed
        if color_var is not None:
            if color_var == "time":
                color_data = self.data.date2num()
            else:
                color_data = self.data[color_var].data
            sc = self.ax.scatter(
                self.data[x].data,
                self.data[y].data,
                c=color_data,
                cmap=self.get_cmap(color_var),
                vmin = self.data[color_var].vmin,
                vmax = self.data[color_var].vmax, **kwargs
            )
            self.add_colorbar(sc, var=color_var)  # Add colorbar

        # If color_var is not passed 
        else:
            sc = self.ax.scatter(self.data[x].data, self.data[y].data, **kwargs)

        self.format_axes(xlabel=self.data[x].get_label(),ylabel=self.data[y].get_label(),invert_yaxis=invert_yaxis)

        return sc
    
    def hovmoller(self, var: str, fig=None, ax=None) -> None:
        """
        Create a scatter plot of depth vs time, with color representing the given variable `var`.
        
        Args:
            var (str): The variable to plot as color.
            fig (matplotlib.figure.Figure, optional): The figure to use for the plot. If None, a new figure is created.
            ax (matplotlib.axes.Axes, optional): The axes to use for the plot. If None, new axes are created.
        
        This method initializes a figure and axes, creates a scatter plot of depth vs. time, and adds a colorbar.
        """
        sc = self.scatter(x='time',
                          y='depth',
                          color_var=var,
                          invert_yaxis=True,
                          ax=ax, fig=fig)
        
        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)

        self.ax.xaxis.set_major_locator(locator)  # Set date locator for x-axis
        self.ax.xaxis.set_major_formatter(formatter)  # Set date formatter for x-axis
        self.format_axes(xlabel=self.data.time.get_label(),ylabel=self.data.depth.get_label())


    def TS(self, color_var=None, fig=None, ax=None, contours: bool = True) -> None:
        """
        Create a temperature vs salinity scatter plot, with optional contours.
        
        Args:
            fig (matplotlib.figure.Figure, optional): The figure to use.
            ax (matplotlib.axes.Axes, optional): The axes to use.
            contours (bool, optional): Whether to include sigma-theta contour lines (default is True).
        
        This method plots salinity vs. temperature, with optional sigma-theta contour lines.
        """
        sc = self.scatter('salinity','temperature',color_var=color_var,fig=fig,ax=ax,zorder=3)  # zorder to put the scatter on top of contours

        if contours:
            # Calculate sigma-theta contours
            Sg, Tg, sigma_theta = get_sigma_theta(
                salinity=self.data['salinity'].data,
                temperature=self.data['temperature'].data
            )
            cs = self.ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1, linestyles='dashed')
            matplotlib.pyplot.clabel(cs, fontsize=10, inline=True, fmt='%.1f')  # Add contour labels

        self.format_axes(xlabel=self.data.salinity.get_label(),ylabel=self.data.temperature.get_label())
        self.ax.set_title('T-S Diagram', fontsize=14, fontweight='bold')  # Add title
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # Set x-axis tick formatting
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

        

    def get_density_color_data(self, color_var: str) -> np.ndarray:
        """
        Retrieve the color data for a variable, or calculate density if requested.
        
        Args:
            color_var (str): The variable for which to retrieve color data.
        
        Returns:
            np.ndarray: The color data for the scatter plot.
        
        If the color variable is 'density' and the instrument does not already have density data, this method 
        calculates it from salinity and temperature.
        """
        if color_var == 'density':
            if not isinstance(self.data['density'], Variable):  # If density is not already provided
                color_data = get_density(
                    self.data['salinity'].data,
                    self.data['temperature'].data
                )  # Calculate density from salinity and temperature
            else:
                color_data = self.data[color_var].data
        else:
            color_data = self.data[color_var].data  # Retrieve color data for the specified variable

        return color_data

    def cross_section(self, longitude, latitude) -> None:
        """
        Method placeholder for plotting cross-sections.

        Args:
            longitude: Longitude line for the cross-section.
            latitude: Latitude line for the cross-section.
        
        Raises:
            NotImplementedError: Indicates that the method is not yet implemented.
        """
        raise NotImplementedError('Need to add method to plot cross sections')
    
    def calculate_quiver_step(self,num_points,quiver_density) -> int:
        """
        Function to calculate the quiver step from the quiver_density
        """
        step = round(num_points/quiver_density)
        return step
    
    def quiver1d(self,x:str,quiver_density:int=None,quiver_scale:float=None,fig=None,ax=None) -> None:
        """
        Method for plotting 1-d quivers. Example: ocean current data at a single location and depth through time.

        Args:
            x: x-axis variable for the quiver.
        """
        self.data.calculate_speed()
        self.data.check_for_vars([x,'u','v','speed'])
        self.init_figure(fig=fig,ax=ax,figsize=(15,5))
        
        # Get the data slice step size using the quiver_density value
        if quiver_density is not None:
            step = self.calculate_quiver_step(len(self.data.u.data),quiver_density)
        elif quiver_density is None:
            step = 1

        # Create the quiver plot
        mappable = self.ax.quiver(self.data[x].data[::step], 0, 
                                        self.data.u.data[::step], self.data.v.data[::step], 
                                        self.data.speed.data[::step], cmap=cmocean.cm.speed,
                                        pivot='tail', scale=quiver_scale, units='height')
        # Add the colorbar
        self.add_colorbar(mappable,'speed')
        self.format_axes(xlabel=self.data[x].get_label(),ylabel=None)
        self.ax.get_yaxis().set_visible(False)

    def quiver2d(self,x:str,y:str,quiver_density:int=None,quiver_scale:float=None,fig=None,ax=None) -> None:
        """
        Method for plotting 2-d quivers. Example: ocean current data at a single location through depth and time.

        Args:
            x (str): x-axis variable for the quiver.
            y (str): y-axis variable for the quiver.
            quiver_density (int): density of quiver arrows. The higher the value the more dense the quivers
            quiver_scale (float|int): Scales the length of the arrow inversely.
            fig (matplotlib.figure.Figure|None): figure to draw the quiver on, if None a new figure will be generated
            ax (matplotlib.axes.Axes|None): axes to draw the quiver on, if None, a new axes will be generated
        """
        self.data.calculate_speed()
        self.data.check_for_vars([x,y,'u','v','speed'])
        self.init_figure(fig=fig,ax=ax)

        # Get the data slice step size using the quiver_density value
        if quiver_density is not None:
            step = self.calculate_quiver_step(len(self.data.u.data),quiver_density)
        elif quiver_density is None:
            step = 1

        # Create the quiver plot
        mappable = self.ax.quiver(self.data[x].data[::step], self.data[y].data[::step], 
                                        self.data.u.data[::step], self.data.v.data[::step], 
                                        self.data.speed.data[::step], cmap=cmocean.cm.speed,
                                        pivot='tail', scale=quiver_scale, units='height')
        # Add the colorbar
        self.add_colorbar(mappable,'speed')
        self.format_axes(xlabel=self.data[x].get_label(),ylabel=self.data[y].get_label())

    def power_spectra_density(self,psd_freq=None,psd=None,
                              var_name:str=None, sampling_freq=None,segment_length=None,theta_rad=None,
                              highlight_freqs:list=None,fig=None,ax=None) -> None:
        '''
        Plot of power spectra density

        You can either pass psd_freq and psd that you calculated
        or 
        You can pass the var_name (string of the variable name), sampling_freq, segment_length, and theta_rad (optional) and let the data.calculate_PSD function calculate it for you

        '''
        # Check if all variables are None         
        if all(var is None for var in [psd_freq, psd, sampling_freq, segment_length]):
            raise ValueError('You must pass either [psd_freq and psd] or [sampling_freq, segment_length, and theta_rad (optional)]')  
             
        # Calculate the power spectra density
        if psd_freq is None or psd is None:
            self.data.calcluate_PSD(sampling_freq,segment_length,theta_rad)
            
        elif psd_freq is not None and psd_freq is not None:
            self.data.add_custom_variable(Variable(psd_freq,name='psd_freq',units='cpd',label='Power Spectra Density Frequency (cpd)'),exist_ok=True)
            self.data.add_custom_variable(Variable(psd,name=f'psd_{var_name}',units='cm²/s²/cpd',label='Power Spectra Density V (cm²/s²/cpd)'),exist_ok=True)

        self.init_figure(fig=fig,ax=ax)
        self.ax.plot(self.data.psd_freq.data, self.data[f'psd_{var_name}'].data, color='blue')
        self.ax.set_xlabel(self.data.psd_freq.get_label())
        self.ax.set_ylabel(self.data[f'psd_{var_name}'].get_label())
        self.ax.set_yscale("log")  # Log scale for PSD
        self.ax.set_xscale("log")  # Log scale for frequency
        self.ax.grid(True, which="both", linestyle="--", linewidth=0.5)
        # Add highlight freqencies
        if highlight_freqs is not None:
            _ = [self.ax.axvline(highlight_freq, color=plt.get_cmap('tab10')(idx), linestyle='--', linewidth=1, label=f'{highlight_freq:.3f} cpd') for idx,highlight_freq in enumerate(highlight_freqs)]
            self.ax.legend()
        self.fig.suptitle(f'Power Spectra Density',fontsize=22)

    def tricontourf(self,x:str,y:str,z:str,fig=None,ax=None):
        '''Create contourf of irregularly gridded data'''
        # Check if vars are present
        self.data.check_for_vars([x,y,z])
        self.init_figure(fig=None,ax=None)
        self.ax.tricontourf(self.data[x].data,self.data[y].data,self.data[z].data,cmap=self.data[z].cmap)
        self.format_axes(xlabel=self.data[x].get_label(),ylabel=self.data[y].get_label())






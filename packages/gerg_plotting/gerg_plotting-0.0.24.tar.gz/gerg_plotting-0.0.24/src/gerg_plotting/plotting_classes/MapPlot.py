from attrs import define, field
import matplotlib.colorbar
import matplotlib.collections
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.axes_divider import AxesDivider
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.gridliner
import cmocean
import numpy as np

from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.data_classes.Bathy import Bathy


@define
class MapPlot(Plotter):
    """
    A class for plotting geographic data on a map using Cartopy and Matplotlib.
    It provides functionality to plot bathymetry, scatter plots, and configure the map with coastlines, grids, and colorbars.
    
    Attributes:
    - bathy (Bathy): Object containing bathymetric data for the map.
    - sc (PathCollection): Matplotlib object for scatter plots.
    - gl (Gridliner): Object for managing gridlines on the map.
    - cbar_var (Colorbar): Colorbar for the variable being visualized (e.g., temperature, salinity).
    - cbar_bathy (Colorbar): Colorbar for the bathymetry.
    - grid_spacing (int): Spacing for the gridlines on the map (default is 1 degree).
    """
    
    bathy: Bathy = field(default=None)  # Bathymetry data object
    sc: matplotlib.collections.PathCollection = field(init=False)  # Scatter plot collection
    gl: cartopy.mpl.gridliner.Gridliner = field(init=False)  # Gridliner for controlling map gridlines
    cbar_var: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for the variable being plotted
    cbar_bathy: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for bathymetry data
    grid_spacing: int = field(default=1)  # Spacing of the gridlines on the map in degrees


    def init_bathy(self) -> None:
        """
        Initializes the bathymetry object if it's not already provided.
        If no bathymetry object is passed, it creates one based on the current map bounds.
        """
        if not isinstance(self.bathy, Bathy):
            self.bathy = Bathy(bounds=self.data.bounds)

    def set_up_map(self, fig=None, ax=None, var=None) -> tuple[str,Colormap,AxesDivider]|tuple[np.ndarray,Colormap,AxesDivider]:
        """
        Sets up the figure and axis for the map plot, including axis limits, color maps, and dividers for colorbars.
        
        Parameters:
        - fig (Figure): Matplotlib figure object.
        - ax (Axes): Matplotlib axes object for the map.
        - var (str | None): Variable name for color mapping (e.g., temperature, salinity).

        Returns:
        - color (str | np.ndarray): Color values for scatter plot points.
        - cmap (Colormap | None): Colormap for the scatter plot.
        - divider (AxesDivider): Divider object for placing colorbars.
        """
        # Ensure the bounds exists
        self.data.detect_bounds(self.bounds_padding)
        # Ensure the fig and axes exist
        self.init_figure(fig=fig, ax=ax, geography=True)
        
        if var is None:
            color = 'k'  # Use black color if no variable is provided
            cmap = None
        else:
            if var == 'time':
                color_var_values = np.array(self.data.date2num())
            else:
                color_var_values = self.data[var].data.copy()
            color = color_var_values  # Color is determined by the variable data
            cmap = self.get_cmap(var)  # Get the appropriate colormap for the variable
        
        if self.data.bounds is not None:
            self.ax.set_extent([self.data.bounds.lon_min, self.data.bounds.lon_max,
                                self.data.bounds.lat_min, self.data.bounds.lat_max])  # Set map extent
        
        divider = make_axes_locatable(self.ax)  # Create a divider for colorbars
        return color, cmap, divider

    def add_coasts(self,show_coastlines) -> None:
        """
        Adds coastlines to the map.
        """
        if show_coastlines:
            self.ax.coastlines()

    def get_quiver_step(self,quiver_density) -> int|None:
        """Calculate the step size for slicing the data to change the density of the quiver plot"""
        if quiver_density is not None:
            step = round(len(self.data.u.data)/quiver_density)
        else:
            step = None
        return step

    def add_grid(self,grid:bool,show_coords:bool=True) -> None:
        # Add gridlines if requested
        if grid:
            self.gl = self.ax.gridlines(draw_labels=True, linewidth=1, color='gray',
                                        alpha=0.4, linestyle='--')
            self.gl.xlocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for x-axis
            self.gl.ylocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for y-axis
        else:
            self.gl = self.ax.gridlines(draw_labels=True, linewidth=1, color='gray',
                                        alpha=0.0, linestyle='--')
            self.gl.xlocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for x-axis
            self.gl.ylocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for y-axis
        if show_coords:
            self.gl.top_labels = False  # Disable top labels
            self.gl.right_labels = False  # Disable right labels
            self.gl.xformatter = LONGITUDE_FORMATTER  # Format x-axis as longitude
            self.gl.yformatter = LATITUDE_FORMATTER  # Format y-axis as latitude
        else:
            self.gl.top_labels = False  # Disable top labels
            self.gl.right_labels = False  # Disable right labels
            self.gl.bottom_labels = False  # Disable top labels
            self.gl.left_labels = False  # Disable right labels

    def add_bathy(self, show_bathy, divider) -> None:
        """
        Adds bathymetric data to the map as a filled contour plot, and creates a colorbar for it.
        
        Parameters:
        - show_bathy (bool): Whether to display bathymetric data.
        - divider (AxesDivider): Divider object for placing the bathymetry colorbar.
        """
        if show_bathy:
            self.init_bathy()
            bathy_contourf = self.ax.contourf(self.bathy.lon, self.bathy.lat, self.bathy.depth,
                                              levels=self.bathy.contour_levels, cmap=self.bathy.cmap,
                                              vmin=self.bathy.vmin, transform=ccrs.PlateCarree(), extend='both')
            # Add a colorbar for the bathymetry
            self.cbar_bathy = self.bathy.add_colorbar(mappable=bathy_contourf, divider=divider,
                                                      fig=self.fig, nrows=self.nrows)

    def scatter(self, var: str | None = None, show_bathy: bool = True, show_coastlines:bool=True, pointsize=3, linewidths=0, grid=True,show_coords=True, fig=None, ax=None) -> None:
        """
        Plots a scatter plot of points on the map, optionally including bathymetry and gridlines.
        
        Parameters:  
        - var (str | None): The name of the variable to plot as color (e.g., temperature).
        - show_bathy (bool): Whether to show bathymetric data.
        - pointsize (int): Size of scatter plot points (default is 3).
        - linewidths (int): Line width of scatter plot points (default is 0).
        - grid (bool): Whether to display gridlines on the map (default is True).
        - fig (Figure): Matplotlib figure object (optional).
        - ax (Axes): Matplotlib axes object (optional).
        """
        color, cmap, divider = self.set_up_map(fig=fig, ax=ax, var=var)
        

        # Add bathymetry if needed
        self.add_bathy(show_bathy, divider)
        
        # Plot scatter points on the map
        self.sc = self.ax.scatter(self.data['lon'].data, self.data['lat'].data, linewidths=linewidths,
                                  c=color, cmap=cmap, s=pointsize, transform=ccrs.PlateCarree(),vmin=self.data[var].vmin,vmax=self.data[var].vmax)
        # Add a colorbar for the scatter plot variable
        self.cbar_var = self.add_colorbar(self.sc, var, divider, total_cbars=(2 if show_bathy else 1))

        self.add_coasts(show_coastlines)  # Add coastlines
        
        self.add_grid(grid=grid,show_coords=show_coords)


    def quiver(self,x:str='lon',y:str='lat',quiver_density:int=None,quiver_scale:float=None,grid:bool=True,show_bathy:bool=True,show_coastlines:bool=True,fig=None,ax=None) -> None:
        """
        Method for plotting 2-d quivers. Example: ocean current data at a single location through depth and time.

        Args:
            x (str): x-axis variable for the quiver.
            y (str): y-axis variable for the quiver.
            quiver_density (int): density of quiver arrows. The higher the value the more dense the quivers
            quiver_scale (float|int): Scales the length of the arrow inversely.
        """
        # Ensure that data has speed
        self.data.calculate_speed(include_w=False)

        # Set up the map
        _, cmap, divider = self.set_up_map(fig=fig, ax=ax, var='speed')
        
        # Add bathymetry if needed
        self.add_bathy(show_bathy, divider)

        step = self.get_quiver_step(quiver_density)

        mappable = self.ax.quiver(self.data[x].data[::step], self.data[y].data[::step], 
                                        self.data.u.data[::step], self.data.v.data[::step], 
                                        self.data.speed.data[::step], cmap=cmap,
                                        pivot='tail', scale=quiver_scale, units='height')
        self.cbar_var = self.add_colorbar(mappable, 'speed', divider, total_cbars=(2 if show_bathy else 1))
        
        self.add_coasts(show_coastlines)  # Add coastlines

        self.add_grid(grid)
        
        

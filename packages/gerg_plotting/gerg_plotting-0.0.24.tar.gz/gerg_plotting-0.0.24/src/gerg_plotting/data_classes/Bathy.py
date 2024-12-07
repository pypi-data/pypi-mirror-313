import matplotlib.figure
import numpy as np
from attrs import define,field
import matplotlib.axes
import matplotlib.pyplot
import matplotlib.colorbar
from matplotlib.colors import Colormap
import xarray as xr
from pathlib import Path
import cmocean

from gerg_plotting.modules.calculations import get_center_of_mass
from gerg_plotting.modules.plotting import colorbar
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.Bounds import Bounds


@define(repr=False)
class Bathy(SpatialInstrument):
    # Vars
    bounds:Bounds = field(default=None)
    resolution_level:float|int|None = field(default=5)
    contour_levels:int = field(default=50)
    land_color:list = field(default=[231/255,194/255,139/255,1])
    vmin:int|float = field(default=0)
    cmap:Colormap = field(default=matplotlib.colormaps.get_cmap('Blues'))
    cbar_show:bool = field(default=True)
    cbar:matplotlib.colorbar.Colorbar = field(init=False)
    cbar_nbins:int = field(default=5)
    cbar_kwargs:dict = field(default={})
    center_of_mass:tuple = field(init=False)
    label:str = field(default='Bathymetry')


    def __attrs_post_init__(self) -> None:
        self.get_bathy()
        if self.bounds.vertical_scaler is not None:
            self.depth = self.depth*self.bounds.vertical_scaler
        self.center_of_mass = get_center_of_mass(self.lon,self.lat,self.depth)
        self.adjust_cmap()


    def get_label(self) -> str:
        # if the user provided units, we will use them
        if self.bounds.vertical_units != '':
            self.label = f"Bathymetry ({self.bounds.vertical_units})"
        return self.label
        

    def adjust_cmap(self) -> None:
        # Remove the white most but of the colormap
        self.cmap = cmocean.tools.crop_by_percent(self.cmap,20,'min')
        # Add land color to the colormap
        self.cmap.set_under(self.land_color)


    def get_bathy(self) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
        '''
        bounds (Bounds): contains attributes of lat_min,lon_min,lat_max,lon_max,depth_max,depth_min
        resolution_level (float|int): how much to coarsen the dataset by in units of degrees

        returns:
        lon,lat,depth
        '''
        if self.bounds is None:
            raise ValueError(f'The map bounds are not found')
        
        self_path = Path(__file__).parent
        seafloor_path = self_path.parent.joinpath('seafloor_data/seafloor_data.nc')
        ds = xr.open_dataset(seafloor_path) #read in seafloor data

        ds = ds.sel(lat=slice(self.bounds["lat_min"],self.bounds["lat_max"])).sel(lon=slice(self.bounds["lon_min"],self.bounds["lon_max"])) #slice to the focus area

        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level,boundary='trim').mean().coarsen(lon=self.resolution_level,boundary='trim').mean() #coarsen the seafloor data (speed up figure drawing) #type:ignore

        self.depth = ds['elevation'].values*-1 #extract the depth values and flip them
    
        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth>self.bounds["depth_top"],self.depth,self.bounds["depth_top"]) #set all depth values less than the depth_top to the same value as depth_top for visuals
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth<self.bounds["depth_bottom"],self.depth,self.bounds["depth_bottom"]) #set all depth values less than the depth_bottom to the same value as depth_bottom for visuals

        self.lon = ds.coords['lat'].values #extract the latitude values
        self.lat = ds.coords['lon'].values #extract the longitude values
        self.lon, self.lat = np.meshgrid(self.lat, self.lon) #create meshgrid for plotting

        return self.lon,self.lat,self.depth
    
    
    def add_colorbar(self,fig:matplotlib.figure.Figure,divider,mappable:matplotlib.axes.Axes,nrows:int) -> None:
        if self.cbar_show:
            label = self.get_label()
            self.cbar = colorbar(fig,divider,mappable,label,nrows=nrows)
            self.cbar.ax.locator_params(nbins=self.cbar_nbins)
            self.cbar.ax.invert_yaxis()
            return self.cbar


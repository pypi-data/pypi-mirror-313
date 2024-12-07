'''
A module for standardized plotting at GERG
'''

from .plotting_classes.Histogram import Histogram
from .plotting_classes.Animator import Animator
from .data_classes.Bounds import Bounds
from .data_classes.Variable import Variable
from .data_classes.Bathy import Bathy
from .data_classes.Data import Data
from .plotting_classes.MapPlot import MapPlot
from .plotting_classes.ScatterPlot import ScatterPlot
from .plotting_classes.ScatterPlot3D import ScatterPlot3D
from .plotting_classes.CoveragePlot import CoveragePlot
from .tools import data_from_df,data_from_csv,interp_glider_lat_lon
import cmocean

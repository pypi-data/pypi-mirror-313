# CoveragePlot.py

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colors import Colormap
from matplotlib.ticker import FixedLocator
from matplotlib.text import Text
from matplotlib.patches import Rectangle,FancyArrow
from attrs import define,field,asdict
from pprint import pformat
import itertools

from gerg_plotting.modules.utilities import extract_kwargs_with_aliases
from gerg_plotting.tools import normalize_string,merge_dicts



@define
class Base:

    def _has_var(self, key) -> bool:
        '''Check if object has var'''
        return key in asdict(self).keys()
    
    def get_vars(self) -> list:
        '''Get list of object variables/attributes'''
        return list(asdict(self).keys())

    def __getitem__(self, key: str):
        '''
        Allow dictionary-style access to class attributes.
        
        Args:
            key (str): The attribute name to access.
        
        Returns:
            The value of the specified attribute.
        '''
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")  

    def __setitem__(self, key, value) -> None:
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")

    def __str__(self) -> None:
        '''Return a pretty-printed string representation of the class attributes.'''
        return pformat(asdict(self),width=1)



@define
class Grid(Base):
    xlabels:list
    ylabels:list
    # Defaults
    grid_linewidth:float = field(default=1)
    grid_linestyle:str = field(default='--')
    grid_color:str|tuple = field(default='black')
    grid_zorder:float = field(default=1.15)

    def add_hlines(self,ax:Axes,y_values,**kwargs):
        zorder = kwargs.pop('zorder',self.grid_zorder)
        for y_value in y_values:
            ax.axhline(y_value,zorder=zorder,**kwargs)

    def add_vlines(self,ax:Axes,x_values,**kwargs):
        zorder = kwargs.pop('zorder',self.grid_zorder)
        for x_value in x_values:
            ax.axvline(x_value,zorder=zorder,**kwargs)

    def add_grid(self,ax,**grid_kwargs):
        defaults = {'grid_linewidth': self.grid_linewidth,
                    'grid_color': self.grid_color,'grid_linestyle': self.grid_linestyle}

        linewidth, color, linestyle  = extract_kwargs_with_aliases(grid_kwargs, defaults).values()
        n_hlines = len(self.ylabels)
        n_vlines = len(self.xlabels)
        self.add_hlines(ax=ax,y_values=np.arange(-0.5,n_hlines+0.5,1),linewidth=linewidth,ls=linestyle,color=color)
        self.add_vlines(ax=ax,x_values=np.arange(0,n_vlines+1,1),linewidth=linewidth,ls=linestyle,color=color)

@define
class ExtentArrows(Base):
    # Defaults
    arrow_facecolor:str|tuple = field(default='black') # If "coverage_color" then the arrow's facecolor will be the color of the corresponding coverage's facecolor
    arrow_edgecolor:str|tuple = field(default='black')
    arrow_tail_width:float = field(default=0.05)
    arrow_head_width:float = field(default=0.12)
    arrow_zorder:float = field(default=2.9)
    arrow_linewidth:float = field(default=0)
    arrow_text_padding:float = field(default=0.05)
    # Add other defaults too
    # Arrows
    left_arrow:FancyArrow = field(default=None)
    right_arrow:FancyArrow = field(default=None)
    top_arrow:FancyArrow = field(default=None)
    bottom_arrow:FancyArrow = field(default=None)

    def calculate_arrow_length(self,ax:Axes,rect,text_left,text_right):
        rect_bbox = ax.transData.inverted().transform(rect.get_window_extent())

        rect_left, rect_bottom = rect_bbox[0]
        rect_right, rect_top = rect_bbox[1]

        left_arrow_length = rect_left-text_left
        right_arrow_length = rect_right-text_right

        return left_arrow_length,right_arrow_length


    def add_range_arrows(self,ax:Axes,text:Text,rect:Rectangle):
        
        if self.arrow_facecolor=='coverage_color':
            self.arrow_facecolor = rect.get_facecolor()
        elif self.arrow_facecolor=='hatch_color':
            self.arrow_facecolor = rect.get_edgecolor()

        text_bbox = ax.transData.inverted().transform(text.get_window_extent())

        # Calculate the left and right bounds of the text in data coordinates
        text_left, text_bottom = text_bbox[0]
        text_right, text_top = text_bbox[1]
        text_y_center = (text_bottom + text_top) / 2  # The vertical center of the text

        arrow_props = {'width': self.arrow_tail_width, 'facecolor': self.arrow_facecolor,'head_width':self.arrow_head_width,
                       "length_includes_head":True,'zorder':self.arrow_zorder,
                       'edgecolor':self.arrow_edgecolor,'linewidth':self.arrow_linewidth}

        left_arrow_length,right_arrow_length = (self.calculate_arrow_length(ax,rect,text_left=text_left,text_right=text_right))

        left_arrow_left_bound = text_left - self.arrow_text_padding
        left_arrow_right_bound = left_arrow_length + self.arrow_text_padding

        right_arrow_left_bound = text_right + self.arrow_text_padding
        right_arrow_right_bound = right_arrow_length - self.arrow_text_padding

        left_arrow = FancyArrow(left_arrow_left_bound, text_y_center, left_arrow_right_bound, 0, **arrow_props)
        right_arrow = FancyArrow(right_arrow_left_bound, text_y_center, right_arrow_right_bound, 0, **arrow_props)

        ax.add_artist(left_arrow)
        ax.add_artist(right_arrow)


@define
class Coverage(Base):
    body:Rectangle = field(init=False)
    outline:Rectangle = field(init=False)
    label:Text = field(init=False)
    extent_arrows:ExtentArrows = field(init=False)

    # Body Default Parameters
    body_min_height:float = field(default=0.25)
    body_alpha:float = field(default=1)
    body_linewidth:float = field(default=1)
    body_color:str|tuple = field(default='none')
    body_hatch:str = field(default=None)
    body_hatch_color:str = field(default=None)
    hatch_linewidth:float = field(default=0.5)
    # Outline Default Parameters
    outline_edgecolor:str|tuple = field(default='k')
    outline_alpha:float = field(default=1)
    outline_linewidth:float = field(default=1)
    # Label Default Parameters
    label_fontsize:float = field(default=12)
    label_background_pad:float = field(default=2)
    label_background_linewidth:float = field(default=0)
    label_background_alpha:float = field(default=1)
    label_background_color:float = field(default='body_color')

    def create(self,xrange,yrange,label,**kwargs):
        # Bottom left corner
        anchor_point = (xrange[0],yrange[0])

        width = (xrange[1] - xrange[0])

        height = (yrange[1] - yrange[0])

        body_defaults = {('body_alpha'): self.body_alpha,('body_linewidth'): self.body_linewidth,
                         ('body_color'):self.body_color,('hatch','body_hatch'):self.body_hatch,
                         ('body_hatch_color','hatch_color'):self.body_hatch_color,'hatch_linewidth':self.hatch_linewidth,
                         'body_min_height':self.body_min_height}
        
        outline_defaults = {('outline_edgecolor'): self.outline_edgecolor,'body_outline_alpha':self.outline_alpha,'outline_linewidth':self.outline_linewidth}
        
        label_defaults = {'label': label,'label_fontsize':self.label_fontsize,'label_background_pad':self.label_background_pad,
                          'label_background_linewidth':self.label_background_linewidth,'label_background_alpha':self.label_background_alpha,
                          'label_background_color':self.label_background_color}
        

        self.body_alpha,self.body_linewidth,self.body_color,self.body_hatch,self.body_hatch_color,self.hatch_linewidth,self.body_min_height = extract_kwargs_with_aliases(kwargs, body_defaults).values()

        self.outline_edgecolor,self.outline_alpha,self.outline_linewidth = extract_kwargs_with_aliases(kwargs, outline_defaults).values()

        self.label,self.label_fontsize,self.label_background_pad,self.label_background_linewidth,self.label_background_alpha,self.label_background_color = extract_kwargs_with_aliases(kwargs, label_defaults).values()
        
        if height == 0:
            height = self.body_min_height

        if self.label_background_color=='hatch_color':
            self.label_background_color=self.body_hatch_color
        elif self.label_background_color=='body_color':
            self.label_background_color=self.body_color
        else:
            self.label_background_color = self.label_background_color

        matplotlib.rcParams['hatch.linewidth'] = self.hatch_linewidth

        # Init body
        body = Rectangle(anchor_point,width=width,height=height,
                         fc=self.body_color,alpha=self.body_alpha,
                         linewidth=self.body_linewidth,edgecolor=self.body_hatch_color,
                         label=label,hatch=self.body_hatch)
        
        # Init outline
        outline = Rectangle(anchor_point,width=width,height=height,fc=None,fill=False,alpha=self.outline_alpha,
                         linewidth=self.outline_linewidth, edgecolor = self.outline_edgecolor,
                         label=None,zorder=body.get_zorder()+0.1)  # put outline on top of body
        

        label_position = kwargs.pop('label_position',body.get_center())

        text = Text(*label_position,text=label,fontsize=self.label_fontsize,ha='center',va='center',zorder=5)

        self.body = body
        self.outline = outline
        self.label = text

        self.extent_arrows = ExtentArrows(**kwargs)

        return self
    
    def add_label_background(self,text:Text):
        text.set_bbox(dict(facecolor=self.label_background_color,pad=self.label_background_pad,
                           linewidth=self.label_background_linewidth,alpha=self.label_background_alpha))

    def plot(self,ax:Axes,**kwargs):
        ax.add_artist(self.body)
        ax.add_artist(self.outline)
        ax.add_artist(self.label)
        self.add_label_background(self.label)
        self.extent_arrows.add_range_arrows(ax=ax,text=self.label,rect=self.body,**kwargs)




@define
class CoveragePlot(Base):
    fig:Figure = field(default=None)
    ax:Axes = field(default=None)
    figsize:tuple = field(default=None)

    horizontal_padding:float = field(default=0.25)
    vertical_padding:float = field(default=0.75)

    xlabels:list = field(default=None)
    ylabels:list = field(default=None)

    cmap:str|Colormap = field(default=None)
    color_iterator:itertools.cycle = field(init=False)

    coverages:list[Coverage] = field(factory=list)
    coverage_color_default = field(default=None)

    grid:Grid = field(init=False)

    plotting_kwargs:dict = field(default={})


    def __attrs_post_init__(self):
        """
        Initializes the ColorCycler and the coverages container

        :param colormap_name: Name of the matplotlib colormap to use.
        :param n_colors: Number of discrete colors to divide the colormap into.
        """
        if self.cmap is None:
            self.cmap = plt.get_cmap('tab10')
        elif isinstance(self.cmap,str):
            self.cmap = plt.get_cmap(self.cmap)
        elif isinstance(self.cmap,Colormap):
            self.cmap = self.cmap
        n_colors = self.cmap.N
        self.color_iterator = itertools.cycle(
            (self.cmap(i / (n_colors - 1)) for i in range(n_colors))
        )

        self.grid = Grid(xlabels=self.xlabels,ylabels=self.ylabels)


    def coverage_color(self):
        """
        A generator that yields the next color in the colormap cycle.

        :yield: A tuple representing an RGBA color.
        """
        if self.coverage_color_default is None:
            return next(self.color_iterator)
        else:
            return self.coverage_color_default
        
    def handle_ranges(self,xrange,yrange):
        '''
        If the user used label names/strings to identify the x and y ranges,
        we need to convert those to numeric so we can plot it
        '''

        xlabel_dict = {normalize_string(value):idx for idx,value in enumerate(self.xlabels)}
        ylabel_dict = {normalize_string(value):idx for idx,value in enumerate(self.ylabels)}

        # Handle using labels for position
        for idx,x in enumerate(xrange):
            # If the user passed a string for the position
            if isinstance(x,str):
                # Normalize the key
                x = normalize_string(x)
                # Assign the xrange to its value as an integer
                xrange[idx] = xlabel_dict[x]
                # Add one to the max value of the xrange
                if idx == 1:
                    xrange[1]+=1

        for idx,y in enumerate(yrange):
            if isinstance(y,str):
                y = normalize_string(y)
                yrange[idx] = ylabel_dict[y]
                if idx == 1:
                    yrange[1]+=0.5
                if idx == 0:
                    yrange[0]-=0.5

        return xrange,yrange


    def add_coverage(self,xrange,yrange,label,**kwargs):
        '''
        xrange (list): A list of values containing the x coverage range
        yrange (list): A list of values containing the y coverage range

        Turn off the label on top of the coverage, but keep the label in the legend, pass `visible = False`
        '''
        # Init test values
        if not isinstance(xrange,list):
            xrange = [xrange]
        if not isinstance(yrange,list):
            yrange = [yrange]

        if len(xrange)==1:
            xrange.extend(xrange)
        if len(yrange)==1:
            yrange.extend(yrange)

        # If both xrange and yrange contain the same number of values
        if len(xrange) == len(yrange):
            xrange,yrange = self.handle_ranges(xrange=xrange,yrange=yrange)
            # Init the coverage and add it to the list
            # Add figure wide kwargs to coverage wide kwargs
            kwargs = merge_dicts(self.plotting_kwargs,kwargs)
            body_color = kwargs.pop('body_color',self.coverage_color())
            coverage = Coverage().create(xrange=xrange,yrange=yrange,label=label,body_color=body_color,**kwargs)
            self.coverages.extend([coverage])
            return
        else:
            raise ValueError(f'xrange and yrange must both be the same length {xrange = }, {yrange = }')
    

    def save(self,filename,**kwargs):
        '''
        Save the current figure
        '''
        if self.fig is not None:
            self.fig.savefig(fname=filename,**kwargs)
        else:
            raise ValueError('No figure to save')
        
    def show(self,**kwargs):
        '''
        Show all open figures
        '''
        plt.show(**kwargs)

    def init_figure(self) -> None:
        '''
        Initialize the figure and axes if they are not provided.
        
        Args:
            fig (matplotlib.figure.Figure, optional): Pre-existing figure.
            ax (matplotlib.axes.Axes, optional): Pre-existing axes.
            three_d (bool, optional): Flag to initialize a 3D plot.
            geography (bool, optional): Flag to initialize a map projection (Cartopy).
        
        Raises:
            ValueError: If both 'three_d' and 'geography' are set to True.
        '''

        if self.fig is None and self.ax is None:
            # Standard 2D Matplotlib figure
            self.fig, self.ax = plt.subplots(figsize=self.figsize)

    def custom_ticks(self,labels,axis:str):
        # Set custom ticks and labels

        if axis.lower() == 'x':
            major_locator = self.ax.xaxis.set_major_locator
            label_setter = self.ax.set_xticklabels
            tick_positions = np.arange(0.5,len(labels)+0.5)  # Tick positions
            
        elif axis.lower() == 'y':
            major_locator = self.ax.yaxis.set_major_locator
            label_setter = self.ax.set_yticklabels  
            tick_positions = np.arange(0,len(labels))  # Tick positions     

        major_locator(FixedLocator(tick_positions))
        label_setter(labels)
        self.ax.tick_params('both',length=0)

    def set_padding(self):
        xmin = 0 - self.horizontal_padding
        xmax = len(self.xlabels)+self.horizontal_padding

        ymin = 0 - self.vertical_padding
        ymax = len(self.ylabels)-1+self.vertical_padding

        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)

    def add_grid(self,show_grid:bool):
        if show_grid:
            self.grid.add_grid(ax=self.ax)

    def set_up_plot(self,show_grid:bool=True):
        # Init figure
        self.init_figure()
        # Set custom ticks and labels
        self.custom_ticks(labels=self.ylabels,axis='y')
        self.custom_ticks(labels=self.xlabels,axis='x')
        # Show the grid
        self.add_grid(show_grid)
        # Add padding to the border
        self.set_padding()
        # invert the y-xais
        self.ax.invert_yaxis()
        # Put the x-axis labels on top
        self.ax.tick_params(axis='x', labeltop=True, labelbottom=False)
        # Set layout to tight
        self.fig.tight_layout()

    def plot_coverages(self):
        for coverage in self.coverages:
            coverage.plot(self.ax)

    def plot(self,show_grid=True):
        self.set_up_plot(show_grid=show_grid)
        self.plot_coverages()

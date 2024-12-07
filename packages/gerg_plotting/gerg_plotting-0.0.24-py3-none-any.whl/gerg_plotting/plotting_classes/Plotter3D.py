from attrs import define, asdict, field
from pprint import pformat
import numpy as np
import mayavi.core.lut_manager
import mayavi.core.scene
import mayavi.mlab as mlab

from gerg_plotting.data_classes.Data import Data
from gerg_plotting.data_classes.Bathy import Bathy

@define
class Plotter3D:
    """
    Base class providing 3D plotting functionalities using Mayavi for SpatialInstrument data.

    Attributes:
        data (SpatialInstrument): Spatial data object containing longitude, latitude, and variable data.
        bathy (Bathy): Bathymetry data used for adding depth information to 3D plots.
        fig (mayavi.core.scene.Scene): Figure object for 3D visualizations.
        figsize (tuple): Size of the figure window in pixels (width, height).
    """
    data: Data
    bathy: Bathy = field(default=None)
    fig: mayavi.core.scene.Scene = field(default=None)
    figsize: tuple = field(default=(1920, 1080))


    def init_figure(self, fig=None):
        """
        Initialize a new Mayavi figure or use an existing one if provided.

        Args:
            fig (mayavi.core.scene.Scene, optional): Existing figure to use. If None, a new figure is created.

        Returns:
            mayavi.core.scene.Scene: The initialized figure for plotting.
        """
        # Check if a new figure needs to be created
        if fig is None:
            fig = mlab.figure(size=self.figsize)  # Create figure with specified size
        elif isinstance(fig, mayavi.core.scene.Scene):
            fig = fig  # Use existing figure if of correct type
        else:
            raise ValueError("fig must be either None or a mayavi.core.scene.Scene object")
        return fig
    

    def _has_var(self, key) -> bool:
        """
        Check if the object has an attribute with the specified key.

        Args:
            key (str): Attribute name to check for.

        Returns:
            bool: True if attribute exists, False otherwise.
        """
        # Check if key exists in the object's dictionary representation
        return key in asdict(self).keys()
    

    def get_vars(self) -> list:
        """
        Retrieve a list of all object attributes.

        Returns:
            list: List of attribute names for this object.
        """
        # Get list of attributes by converting object to dictionary
        return list(asdict(self).keys())


    def __getitem__(self, key: str):
        """
        Access class attributes using dictionary-style indexing.

        Args:
            key (str): The attribute name to access.

        Returns:
            The value of the specified attribute.
        """
        # Check for existence of the attribute
        if self._has_var(key):
            return getattr(self, key)  # Return attribute value if found
        raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")  


    def __setitem__(self, key, value):
        """
        Set class attributes using dictionary-style indexing.

        Args:
            key (str): The attribute name to set.
            value: The value to assign to the attribute.
        """
        # Check for existence of the attribute
        if self._has_var(key):
            setattr(self, key, value)  # Set attribute value if found
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self.get_vars()}")


    def __repr__(self) -> None:
        """
        Pretty-print the class attributes for improved readability.

        Returns:
            str: A formatted string representation of the object.
        """
        # Convert attributes to formatted string for display
        return pformat(asdict(self), width=1)
    

    def show(self):
        """Display the 3D plot in a Mayavi window."""
        mlab.show()


    def save(self,filename,size=None,**kwargs):
        '''
        To save the scene you must do so before you show the scene.

        When saving the scene, set show=False in the plotting method
        Example:
        ```
        # Init the plotter
        three_d = ScatterPlot3D(data)
        three_d.map(show=False)
        three_d.save('map.png')
        # If you would like to see the scene:
        three_d.show()
        ```

        '''
        if isinstance(self.fig,mayavi.core.scene.Scene):
            scene = self.fig.scene
            if scene is not None:
                scene.save(filename,size=size,**kwargs)
            else:
                raise ValueError(f'No scene found. If trying to save a plot, set show=False, then use the save method')


    def convert_colormap(self, colormap, over_color=None, under_color=None) -> np.ndarray:
        """
        Converts a colormap to a color array scaled to 0-255 (uint8) format, allowing customization
        of the first (under_color) and last (over_color) colors in the array.

        Args:
            colormap (Callable): A function generating colors, usually a Matplotlib colormap function.
            over_color (tuple, optional): Color for the highest value in the colormap (e.g., (255, 0, 0) for red).
            under_color (tuple, optional): Color for the lowest value in the colormap.

        Returns:
            np.ndarray: An array of RGBA colors scaled to 0-255, formatted as uint8.
        """
        # Create color array by evaluating colormap across 256 points
        colormap_array = np.array([colormap(i) for i in range(256)])
        colormap_array *= 255  # Scale colors to [0, 255] range for uint8 compatibility
        colormap_array = colormap_array.astype(np.uint8)  # Convert to uint8 for visualization libraries

        # Apply under_color if provided, replacing the first color in the array
        if under_color is not None:
            colormap_array[0] = under_color

        # Apply over_color if provided, replacing the last color in the array
        if over_color is not None:
            colormap_array[-1] = over_color

        return colormap_array


    def format_colorbar(self, colorbar, x_pos1_offset, y_pos1_offset, x_pos2_offset, y_pos2_offset):
        """
        Format the colorbar with adaptive font sizes and offsets for enhanced readability.

        Args:
            colorbar (mayavi.modules.scalarbar.ScalarBar): The colorbar object to be formatted.
        """
        # Calculate font size based on figure height for adaptive scaling
        fontsize = round(((self.figsize[1] / 400) ** 1.8) + 11)
        fontcolor = (0, 0, 0)  # Set text color to black

        colorbar.scalar_bar.unconstrained_font_size = True  # Enable adaptive font sizing
        colorbar.scalar_bar.label_text_property.font_size = fontsize  # Set label font size
        colorbar.scalar_bar.label_text_property.color = fontcolor  # Set label font color
        colorbar.title_text_property.font_size = fontsize  # Set title font size
        colorbar.title_text_property.color = fontcolor  # Set title font color
        colorbar.title_text_property.line_offset = -7  # Adjust offset for better title alignment
        colorbar.title_text_property.line_spacing = 10
        colorbar.title_text_property.vertical_justification = 'top'

        # Adjust position offsets if provided
        if x_pos1_offset is not None or y_pos1_offset is not None:
            pos1 = colorbar.scalar_bar_representation.position
            colorbar.scalar_bar_representation.position = [pos1[0] + x_pos1_offset, pos1[1] + y_pos1_offset]

        if x_pos2_offset is not None or y_pos2_offset is not None:
            pos2 = colorbar.scalar_bar_representation.position2
            colorbar.scalar_bar_representation.position2 = [pos2[0] + x_pos2_offset, pos2[1] + y_pos2_offset]

        return colorbar


    def add_colorbar(self, mappable, cmap_title, over_color=None, x_pos1_offset=None, y_pos1_offset=None,
                     x_pos2_offset=None, y_pos2_offset=None, cmap=None):
        """
        Adds a colorbar to a 3D plot with a custom colormap and formatting.

        Args:
            mappable (mayavi.modules.glyph.Glyph): The 3D data to which the colormap applies.
            cmap_title (str): Title for the colorbar, indicating the data variable it represents.
            cmap (Callable, optional): Custom colormap function. Defaults to default colormap if None.
            over_color (tuple, optional): Color for highest colormap value. Defaults to None.
            x_pos1_offset (float, optional): Horizontal offset for colorbar position. Defaults to None.
            y_pos1_offset (float, optional): Vertical offset for colorbar position. Defaults to None.
            x_pos2_offset (float, optional): Horizontal offset for colorbar end position. Defaults to None.
            y_pos2_offset (float, optional): Vertical offset for colorbar end position. Defaults to None.
        """
        # Apply custom colormap if provided, after conversion for compatibility
        if cmap is not None:
            mappable.module_manager.scalar_lut_manager.lut.table = self.convert_colormap(cmap, over_color=over_color)

        # Create and configure the colorbar for the plot
        colorbar = mlab.colorbar(mappable, orientation='vertical', title=cmap_title, label_fmt='%0.1f', nb_labels=6)
        colorbar.scalar_bar_representation.proportional_resize = True  # Enable proportional resizing

        # Apply colorbar formatting
        colorbar = self.format_colorbar(colorbar, x_pos1_offset=x_pos1_offset, y_pos1_offset=y_pos1_offset,
                                        x_pos2_offset=x_pos2_offset, y_pos2_offset=y_pos2_offset)
        
        return colorbar
        

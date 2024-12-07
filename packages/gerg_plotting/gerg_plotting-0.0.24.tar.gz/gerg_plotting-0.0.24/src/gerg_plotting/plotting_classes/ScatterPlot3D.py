from attrs import define, field
import mayavi.mlab as mlab
import cmocean
import matplotlib.pyplot as plt

from gerg_plotting.plotting_classes.Plotter3D import Plotter3D
from gerg_plotting.data_classes.Bathy import Bathy

@define
class ScatterPlot3D(Plotter3D):
    """
    A class for creating 3D scatter plots using Mayavi, including optional
    bathymetric data and customizable color mapping for variable visualization.
    Inherits from Plotter3D.
    """


    def _check_var(self, var) -> None:
        """
        Check if the provided variable exists in the data object.
        
        Parameters:
            var (str or None): Variable name to check in the data object.
        
        Raises:
            ValueError: If the variable does not exist in the data.
        """
        # Proceed only if a variable is specified
        if var is not None:
            # Verify if the variable exists in the data, raise error if not
            if not self.data._has_var(var):
                raise ValueError(f'Instrument does not have {var}')


    def _points3d(self, var, point_size, fig, vertical_scalar) -> None:
        """
        Plot 3D scatter points for spatial data, with an optional color map for a variable.

        Parameters:
            var (str or None): Variable name to use for color mapping.
            point_size (float): Scale factor for point size.
            fig (mayavi.core.scene.Scene): Figure to plot on.
            vertical_scalar (float or None): Scalar to adjust depth scaling.
        
        Raises:
            ValueError: If the variable is invalid.
        """
        # Rescale depth data if a vertical scalar is specified
        if vertical_scalar is not None:
            self.data['depth'].data = self.data['depth'].data / vertical_scalar

        # Check if a variable is specified
        if var is None:
            # Plot points without variable-based color scaling
            points = mlab.points3d(
                self.data.lon.data, self.data.lat.data, self.data.depth.data,
                mode='sphere', resolution=8, scale_factor=point_size, figure=fig
            )
        elif isinstance(var, str):
            # Plot points with variable-based color scaling
            points = mlab.points3d(
                self.data.lon.data, self.data.lat.data, self.data.depth.data, self.data[var].data,
                mode='sphere', resolution=8, scale_factor=point_size,
                vmax=self.data[var].vmax, vmin=self.data[var].vmin, figure=self.fig
            )
            # Set scaling mode for color mapping
            points.glyph.scale_mode = 'scale_by_vector'
            # Add a colorbar with appropriate settings
            self.add_colorbar(
                mappable=points, cmap_title=self.data[var].get_label(),
                x_pos1_offset=0, y_pos1_offset=0, x_pos2_offset=0, y_pos2_offset=0,
                cmap=self.data[var].cmap
            )
        else:
            # Revert depth scaling if variable input is invalid
            if vertical_scalar is not None:
                self.data['depth'].data = self.data['depth'].data * vertical_scalar
            raise ValueError(f'var must be either None or one of {self.data}')
        
        # Revert depth scaling back to original
        if vertical_scalar is not None:
            self.data['depth'].data = self.data['depth'].data * vertical_scalar


    def _add_bathy(self, fig, bounds_padding, vertical_scaler=None) -> None:
        """
        Add bathymetric data to the 3D plot using a mesh.

        Parameters:
            fig (mayavi.core.scene.Scene): Figure to plot on.
            bounds_padding (float): Padding for bathymetric bounds.
            vertical_scaler (float or None): Scalar for vertical scaling of bathymetric depth.
        """
        # Detect bathymetric bounds if bathy data is not already initialized
        if self.bathy is None:
            bounds = self.data.detect_bounds(bounds_padding=bounds_padding)
            self.bathy = Bathy(bounds=bounds)

        # Retrieve x, y, and z bathymetric coordinates
        x_bathy, y_bathy, z_bathy = self.bathy.get_bathy()

        # Scale z (depth) coordinates if vertical scaler is provided
        if vertical_scaler is not None:
            z_bathy = z_bathy / vertical_scaler

        # Plot bathymetry mesh
        bathy = mlab.mesh(x_bathy, y_bathy, z_bathy, vmax=0, figure=fig)

        # Define land color for regions above water level
        land_color = [231, 194, 139, 255]

        # Modify colormap to fit bathymetry
        bathy_cmap = plt.get_cmap('Blues_r')
        bathy_cmap = cmocean.tools.crop_by_percent(bathy_cmap, 25, 'max')
        bathy_cmap = cmocean.tools.crop_by_percent(bathy_cmap, 18, 'min')

        # Add a colorbar for bathymetric data
        self.add_colorbar(
            mappable=bathy, cmap_title=self.bathy.get_label(), over_color=land_color,
            x_pos1_offset=0.91, y_pos1_offset=0, x_pos2_offset=0, y_pos2_offset=0,
            cmap=bathy_cmap
        )


    def scatter(self, var: str | None = None, point_size: int | float = 0.05, vertical_scalar=None, fig=None, show: bool = True) -> None:
        """
        Create a 3D scatter plot with optional color scaling and depth adjustments.

        Parameters:
            var (str or None): Variable to map color. Defaults to None.
            point_size (int or float): Size of scatter points. Defaults to 0.05.
            vertical_scalar (float or None): Scalar for vertical scaling. Defaults to None.
            fig (mayavi.core.scene.Scene or None): Figure to plot on. Defaults to None.
            show (bool): If True, show the plot. Defaults to True.
        """
        # Initialize the figure or reuse the provided figure
        self.fig = self.init_figure(fig=fig)

        # Check if the specified variable exists
        self._check_var(var=var)

        # Plot the 3D points with the specified settings
        self._points3d(var=var, point_size=point_size, fig=fig, vertical_scalar=vertical_scalar)

        # Display the plot if 'show' is True
        if show:
            self.show()


    def map(self, var: str | None = None, point_size: int | float = 0.05, bounds_padding=0, vertical_scalar=None, fig=None, show: bool = True) -> None:
        """
        Generate a 3D map with bathymetric data and scatter points.

        Parameters:
            var (str or None): Variable to map color. Defaults to None.
            point_size (int or float): Size of scatter points. Defaults to 0.05.
            bounds_padding (float): Padding for bathymetric bounds. Defaults to 0.
            vertical_scalar (float or None): Scalar for vertical scaling. Defaults to None.
            fig (mayavi.core.scene.Scene or None): Figure to plot on. Defaults to None.
            show (bool): If True, show the plot. Defaults to True.
        """
        # Initialize the figure or reuse the provided figure
        self.fig = self.init_figure(fig=fig)

        # Add bathymetry to the plot with specified padding and scaling
        self._add_bathy(fig=fig, bounds_padding=bounds_padding, vertical_scaler=vertical_scalar)

        # Check if the specified variable exists
        self._check_var(var=var)

        # Plot the 3D points with the specified settings
        self._points3d(var=var, point_size=point_size, fig=fig, vertical_scalar=vertical_scalar)

        # Display the plot if 'show' is True
        if show:
            self.show()

from attrs import define, field
from typing import Callable
import io
import os
from pathlib import Path
import imageio.v3 as iio
import imageio
from PIL import Image, ImageFile
import numpy as np
import matplotlib.pyplot as plt

@define
class Animator:
    """
    A class for creating animations (GIFs) from a sequence of images generated 
    by a user-defined plotting function.
    """
    
    # Fields
    plotting_function: Callable = field(init=False)  # Function used to generate frames
    param_list:list[dict] = field(init=False)  # List of dictionaries that contain plotting_function parameter mappings
    num_iterations:int = field(init=False)
    duration: int | float = field(init=False)  # Duration of each frame in the GIF (in ms)
    iteration_param: str = field(init=False)  # The parameter name for the iteration (e.g., azimuth)
    frames: list = field(init=False)  # List to store generated frames in memory
    image_dpi: int = field(default=300)  # DPI (resolution) for saved images

    # Paths and file names for image and GIF handling
    gif_filename: Path = field(init=False)  # Path to save the generated GIF
    images_path: Path = field(init=False)  # Directory for storing temporary images on disk
    image_files: list = field(init=False)  # List of image file paths generated on disk
    function_kwargs: dict = field(init=False)  # Additional arguments for the plotting function

    def __attrs_post_init__(self):
        self.frames = []

    def _restructure_params(self,param_dict) -> list[dict]:
        """
        Restructure a dictionary of parameters, each with an array of values, into
        a list of dictionaries where each dictionary has one value per key.
        
        Checks that all arrays in the dictionary have the same length before restructuring.

        Args:
            param_dict (dict): Dictionary with keys as parameter names and values as arrays.

        Returns:
            list of dict: List of dictionaries where each dictionary represents a single set
                        of values for all parameters.
                        
        Raises:
            ValueError: If the arrays in param_dict do not have the same length, specifying
                        which keys have mismatched lengths.
        """
        # Get the length of the first array in the dictionary as the expected length
        lengths = {key: len(values) for key, values in param_dict.items()}
        expected_length = next(iter(lengths.values()))  # length of the first array
        
        # Find any keys with lengths that differ from the expected length
        mismatched_keys = {key: length for key, length in lengths.items() if length != expected_length}
        if mismatched_keys:
            mismatch_info = ", ".join(f"'{key}': {length}" for key, length in mismatched_keys.items())
            raise ValueError(f"All arrays must have the same length. Expected length {expected_length}, "
                            f"but found mismatches: {mismatch_info}.")
        
        self.num_iterations = expected_length
        
        # Use zip to iterate over values in parallel for all keys
        return [dict(zip(param_dict.keys(), values)) for values in zip(*param_dict.values())]

    def _fig2img(self, fig) -> ImageFile:
        """
        Convert a Matplotlib figure to a PIL Image.

        Parameters:
        fig: The Matplotlib figure to convert.

        Returns:
        ImageFile: The figure converted to a PIL Image.
        """
        # Create an in-memory buffer to store the image data
        buf = io.BytesIO()
        # Save the figure into the buffer with the specified DPI
        fig.savefig(buf, dpi=self.image_dpi)
        # Reset the buffer pointer to the beginning
        buf.seek(0)
        # Open the buffer as a PIL Image and return it
        img = Image.open(buf)
        return img

    def _delete_images(self) -> None:
        """
        Delete image files from disk.
        """
        # Loop through each file path in image_files and remove the file
        for file in self.image_files:
            os.remove(file)

    def _generate_frames_in_memory(self) -> None:
        """
        Generate frames for the animation and store them in memory.
        """
        # Loop over each value in the iterable
        for pair in self.param_list:
            # Call the plotting function with the current iteration value and additional kwargs
            fig = self.plotting_function(**pair, **self.function_kwargs)
            if fig is None:
                raise ValueError('Ensure you are returning the figure in your plotting_function')
            # If the figure is successfully created, convert it to an image
            if fig:
                img = self._fig2img(fig)
                # Append the image to the frames list
                self.frames.append(img)
                # Close the figure to free memory
                plt.close(fig)

    def _generate_frames_on_disk(self) -> None:
        """
        Generate frames for the animation and store them on disk.
        """
        # Calculate the number of digits needed for zero-padding file names
        num_padding = len(str(self.num_iterations))
        # Loop over each value in the iterable
        for idx, pair in enumerate(self.param_list):
            # Create a file name with zero-padded index
            image_filename = self.images_path / f"{idx:0{num_padding}}.png"
            # Call the plotting function with the current iteration value and additional kwargs
            fig = self.plotting_function(**pair, **self.function_kwargs)
            if fig is None:
                raise ValueError('Ensure you are returning the figure in your plotting_function')
            # If the figure is successfully created, save it as a PNG on disk
            if fig:
                fig.savefig(image_filename, dpi=self.image_dpi, format='png')
                # Close the figure to free memory
                plt.close(fig)

    def _save_gif_from_memory(self) -> None:
        """
        Save the GIF from frames stored in memory.
        """
        # Use the first frame as the starting point and append the rest of the frames
        self.frames[0].save(
            self.gif_filename,
            save_all=True,
            append_images=self.frames[1:],
            optimize=True,
            duration=self.duration,  # Set the duration of each frame
            loop=0  # Set the GIF to loop infinitely
        )

    def _save_gif_from_disk(self) -> None:
        """
        Save the GIF from frames stored on disk.
        """
        # Get a sorted list of all PNG files in the images_path
        self.image_files = sorted(self.images_path.glob('*.png'))
        images = []
        # Load each image file and append it to the images list
        for file in self.image_files:
            images.append(imageio.imread(file))
        # Save all loaded images as a GIF
        imageio.mimsave(self.gif_filename, images)

    def animate(self, plotting_function, param_dict, gif_filename: str, fps=24, **kwargs) -> None:
        """
        Create and save a GIF using the provided plotting function and iterable.

        Parameters:
        plotting_function (Callable): The function used to plot each frame.
        iterable (list or np.ndarray): Values over which the plotting function will iterate.
        iteration_param (str): The name of the parameter used for iteration (e.g., 'elev' or 'azim').
        gif_filename (str): The file name (and path) for saving the generated GIF.
        fps (int | float): Frames per second for the GIF (default is 24).
        kwargs: Additional keyword arguments passed to the plotting function.
        """

        # Assign the provided arguments to the corresponding attributes
        self.plotting_function = plotting_function
        self.param_list = self._restructure_params(param_dict=param_dict)
        self.duration = 1000 / fps  # Calculate frame duration in milliseconds
        self.gif_filename = Path(gif_filename)
        self.function_kwargs = kwargs

        # Decide whether to store frames in memory or on disk based on the number of iterations
        if self.num_iterations < 100:
            print(f'Saving figures to memory, n_iterations: {self.num_iterations}')
            self._generate_frames_in_memory()  # Store frames in memory
            self._save_gif_from_memory()  # Save GIF from memory
        else:
            print(f'Saving figures to storage, n_iterations: {self.num_iterations}')
            # Create a directory for storing images if it doesn't exist
            self.images_path = Path(__file__).parent.joinpath('images')
            self.images_path.mkdir(parents=True, exist_ok=True)
            self._generate_frames_on_disk()  # Store frames on disk
            self._save_gif_from_disk()  # Save GIF from disk
            self._delete_images()  # Delete temporary image files from disk

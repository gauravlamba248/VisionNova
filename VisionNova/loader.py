from PIL import Image
import numpy as np
import imageio
from .config import TILE_HEIGHT, TILE_WIDTH, CHANNELS

class Loader:
    @staticmethod
    def load_image(image_path):
        """
        Load an image from the specified file path.

        Parameters:
        image_path (str): The path to the image file to be loaded.

        Returns:
        np.ndarray: A NumPy array representation of the image in RGB format.
        """
        image = Image.open(image_path)
        image = image.convert('RGB')
        image = np.asarray(image)
        if image.shape[-1] != CHANNELS:
            raise RuntimeError(f"INTERNAL ERROR: Failed to convert image to 'RGB'. Image has {image.shape[-1]} channels.")
        if image.shape[0] < TILE_HEIGHT or image.shape[1] < TILE_WIDTH:
            raise ValueError(f"Invalid image size. Image should be at least {TILE_HEIGHT}x{TILE_WIDTH} pixels, but got {image.shape[0]}x{image.shape[1]} pixels.")
        
        return image

    @staticmethod
    def save_image(image:np.ndarray, output_path):
        """
        Save a NumPy array as an image to the specified file path.

        Parameters:
        image (np.ndarray): The NumPy array representing the image to be saved.
        output_path (str): The path where the image will be saved.
        """
        if image.ndim != 3:
            raise RuntimeError(f"INTERNAL ERROR: Image must be a 3D NumPy array (RGB) But has shape : {image.shape}")

        imageio.imwrite(output_path, image)
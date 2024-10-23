from keras.models import load_model
import numpy as np
from .config import TILE_HEIGHT, TILE_WIDTH, CHANNELS

class Model:
    """
    A class to represent a Keras model for image processing.

    This class is responsible for loading a pre-trained Keras model and 
    processing input images to obtain predictions.
    """
    def __init__(self, model_path: str):
        """
        Initializes the Model class by loading a pre-trained Keras model.

        Args:
            model_path (str): The file path to the pre-trained model.
        """
        self.model = load_model(model_path)

    def process_image(self, image: np.ndarray, batch_size: int) -> np.ndarray:
        """
        Processes the input image using the loaded model.

        Args:
            image (np.ndarray): The input image array to be processed.
            batch_size (int): The number of samples per gradient update.

        Returns:
            np.ndarray: The model's predictions for the input image.
        """
        if image.shape[1]!= TILE_HEIGHT or image.shape[2]!=TILE_WIDTH or image.shape[3]!=CHANNELS:
            raise RuntimeError(f"INTERNAL ERROR: Tiles size must be equal to {TILE_HEIGHT}x{TILE_WIDTH}x{CHANNELS} but has shape {image.shape[1:]}")

        processed_output = self.model.predict(image, batch_size=batch_size, verbose=1)
        return processed_output
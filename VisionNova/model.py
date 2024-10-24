from keras.models import load_model
import numpy as np
from .config import TILE_HEIGHT, TILE_WIDTH, CHANNELS

class Model:
    """
    A class to represent a Keras model for image processing.

    This class is responsible for loading a pre-trained Keras model and 
    processing input images to obtain predictions.
    """
    def __init__(self):
        """
        Initializes the Model class.

        """
        self.models = {}

    def load_model(self, model_path: str):
        """
        Loads a Keras model from the specified path, caching it for future use.

        Args:
            model_path (str): The file path to the pre-trained model.

        Returns:
            Model: The loaded Keras model.
        """
        if model_path in self.models:
            return self.models[model_path]

        # Load the model if it hasn't been loaded yet
        model = load_model(model_path)
        self.models[model_path] = model
        return model
    
    def process_image(self, image: np.ndarray, batch_size: int,  model_path: str) -> np.ndarray:

        """
        Processes the input image using the loaded model.

        Args:
            image (np.ndarray): The input image array to be processed.
            batch_size (int): The number of samples per gradient update.

        Returns:
            np.ndarray: The model's predictions for the input image.
        """
        self.load_model(model_path)
        if image.shape[1]!= TILE_HEIGHT or image.shape[2]!=TILE_WIDTH or image.shape[3]!=CHANNELS:
            raise RuntimeError(f"INTERNAL ERROR: Tiles size must be equal to {TILE_HEIGHT}x{TILE_WIDTH}x{CHANNELS} but has shape {image.shape[1:]}")

        processed_output = self.models[model_path].predict(image, batch_size=batch_size, verbose=1)
        return processed_output

from os import path

import numpy as np
from keras.models import load_model

from .config import CHANNELS, TILE_HEIGHT, TILE_WIDTH


class Keras_enhancer:
    """
    A Container for Keras models for image processing.

    This class is responsible for loading a pre-trained Keras model and
    processing input images to obtain predictions.
    """

    def __init__(self, models_dir):
        """
        Initializes the Keras_enhancer class.

        Args:
            models_dir (str): The directory where the pre-trained models are stored.
        """
        self.models_dir = models_dir
        self.model_ext = ".hdf5"
        self.models = {}

    def _model_path(self, models_dir: str, model_name: str):
        return path.join(models_dir, model_name + self.model_ext)

    def _load_model(self, model_name: str):
        if model_name in self.models:
            return self.models[model_name]

        model = load_model(self._model_path(self.models_dir, model_name))
        self.models[model_name] = model
        return model

    def process_image(self, image: np.ndarray, batch_size: int, model_name: str) -> np.ndarray:
        """
        Processes the input image using the loaded model.

        Args:
            image (np.ndarray): The input image array to be processed.
            batch_size (int): The number of samples per gradient update.
            model_name (str): The type of enhancement to be applied.

        Returns:
            np.ndarray: The model's predictions for the input image.
        """
        model = self._load_model(model_name)
        if image.shape[1] != TILE_HEIGHT or image.shape[2] != TILE_WIDTH or image.shape[3] != CHANNELS:
            raise RuntimeError(
                f"INTERNAL ERROR: Tiles size must be equal to {TILE_HEIGHT}x{TILE_WIDTH}x{CHANNELS} but has shape {image.shape[1:]}"
            )

        processed_output = model.predict(image, batch_size=batch_size, verbose=1)
        return processed_output

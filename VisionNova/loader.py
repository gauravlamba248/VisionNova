from PIL import Image
import numpy as np
import imageio

class Loader:
    @staticmethod
    def load_image(image_path):
        image = Image.open(image_path)
        image = image.convert('RGB')
        return image

    @staticmethod
    def save_image(image, output_path):
        image = (image - np.min(image)) / (np.max(image) - np.min(image))  # Normalize to [0, 1]
        image = (image * 255).astype(np.uint8)  # Convert to uint8
        imageio.imwrite(output_path, image)
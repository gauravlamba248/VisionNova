import numpy as np
from .config import TILE_WIDTH, TILE_HEIGHT, OVERLAP, CHANNELS

class ImageUtils:
    """Utility class for image processing tasks"""
    def __init__(self):
        self.image_width = None
        self.image_height = None

    def __split_into_tiles(self, image_array: np.ndarray, tile_width=TILE_WIDTH, tile_height = TILE_HEIGHT, overlap=OVERLAP) -> np.ndarray:
        """
        Splits the input image array into overlapping tiles.

        Args:
            image_array (np.ndarray): The input image array of shape (1, height, width, channels).
            tile_width (int): The width of each tile. Defaults to TILE_WIDTH.
            tile_height (int): The height of each tile. Defaults to TILE_HEIGHT.

            overlap (int): The number of overlapping pixels between tiles. Defaults to OVERLAP.

        Returns:
            np.ndarray: An array of tiles of shape (num_tiles, tile_height, tile_width, channels).
        """
        stride_width = tile_width - overlap
        stride_height = tile_height - overlap
        tiles = []

        height, width, channels = image_array.shape

        for row_start in range(0, height, stride_height):
            row_end = min(row_start + tile_height, height)
            row_start = row_end - tile_height

            for col_start in range(0, width, stride_width):
                col_end = min(col_start + tile_width, width)
                col_start = col_end - tile_width
                
                tile = image_array[row_start:row_end, col_start:col_end, :]
                tiles.append(tile)

        return np.array(tiles)

    def __combine_tiles(self, tiles: np.ndarray, width: int, height: int, tile_width=TILE_WIDTH, tile_height = TILE_HEIGHT, overlap=OVERLAP) -> np.ndarray:
        """
        Combines overlapping tiles back into a single image.

        Args:
            tiles (np.ndarray): An array of tiles of shape (num_tiles, tile_height, tile_width, channels).
            width (int): The width of the original image.
            height (int): The height of the original image.
            tile_width (int): The width of each tile. Defaults to TILE_WIDTH.
            tile_height (int): The height of each tile. Defaults to TILE_HEIGHT.
            overlap (int): The number of overlapping pixels between tiles. Defaults to OVERLAP.

        Returns:
            np.ndarray: The combined image of shape (height, width, channels).
        """
        stride_width = tile_width - overlap
        stride_height = tile_height - overlap
        combined_image = np.zeros((height, width, CHANNELS), dtype=tiles.dtype)
        weight_map = np.zeros((height, width, CHANNELS), dtype=np.float32)

        idx = 0
        for row_start in range(0, height, stride_height):
            row_end = min(row_start+tile_height, height)
            row_start = row_end - tile_height

            for col_start in range(0, width, stride_width):
                col_end = min(col_start+tile_width, width)
                col_start = col_end - tile_width

                combined_image[row_start:row_end, col_start:col_end , :] += tiles[idx][:tile_height, :tile_width, :]
                weight_map[row_start:row_end, col_start:col_end , :] += 1
                idx += 1

        # Avoid division by zero
        weight_map[weight_map == 0] = 1
        combined_image /= weight_map
        return combined_image

    def __to_float32(self, arr: np.ndarray) -> np.ndarray:
        """
        Normalizes the image to the float32 range [0, 1].

        Args:
            arr (np.ndarray): The input array.

        Returns:
            np.ndarray: The converted array as float32.
        """
        return arr.astype(np.float32) / 255

    def __to_uint8(self, arr: np.ndarray) -> np.ndarray:
        """
        Normalizes an array to the range [0, 255] and converts it to uint8.

        Args:
            arr (np.ndarray): The input array.

        Returns:
            np.ndarray: The normalized array as uint8.
        """
        arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))  # Normalize to [0, 1]
        return (arr * 255).astype(np.uint8)  # Convert to uint8

    def pre_process(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocesses the input image.

        Args:
            image (np.ndarray): The input image array of shape (height, width, channels).

        Returns:
            np.ndarray: An array of tiles.
        """
        self.image_height, self.image_width, channels = image.shape
        image = self.__to_float32(image)
        return self.__split_into_tiles(image)

    def post_process(self, tiles: np.ndarray) -> np.ndarray:
        """
        Postprocesses the output tiles.
        Call this function after calling pre_process.

        Args:
            tiles (np.ndarray): An array of tiles.

        Returns:
            np.ndarray: The combined image as uint8.
        """
        if self.image_height is None or self.image_width is None:
            raise RuntimeError(f"INTERNAL ERROR: Image dimensions are not set.")

        combined_image = self.__combine_tiles(tiles, self.image_width, self.image_height)
        return self.__to_uint8(combined_image)
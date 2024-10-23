import numpy as np

WIDTH = 128
HEIGHT = 128
CHANNEL = 3

class Utils:
    @staticmethod
    def pre_process(image):
        image = image.resize((WIDTH, HEIGHT))
        image = np.asarray([image], dtype='uint8').reshape((1, WIDTH, HEIGHT, CHANNEL))
        return image.astype('float32') / 255
    
    @staticmethod
    def post_process(image):
        return image
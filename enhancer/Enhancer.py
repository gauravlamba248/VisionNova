from PIL import Image
import imageio
import numpy as np
from keras.models import load_model

def _load_img(img, shape):
    image = Image.open(img)
    image = image.convert('RGB')
    image = image.resize((shape[0],shape[1]))
    return image

def load_img(img_path, shape):
    width, height, channel = shape
    img = _load_img(img_path, shape)
    return np.asarray([img], dtype='uint8').reshape((1, width, height, channel))

def save_img(img_path, img):
    img = (img - np.min(img)) / (np.max(img) - np.min(img))  # Normalize to 0-1
    img = (img * 255).astype(np.uint8)  # Convert to uint8
    imageio.imwrite(img_path, img)

def load_data(img_path, img_shape):
    image = load_img(img_path, img_shape)
    return image.astype('float32') / 255

def process(model_path, image_path, image_shape, batch_size, output_path):
    model = load_model(model_path)
    image = load_data(image_path, image_shape)
    processed = model.predict(image, batch_size=batch_size, verbose=1)
    save_img(output_path, processed[0])
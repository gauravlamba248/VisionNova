from keras.models import load_model

class Model:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def process_image(self, image, batch_size):
        processed = self.model.predict(image, batch_size=batch_size, verbose=1)
        return processed[0]
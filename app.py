import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import numpy as np
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
from PIL import Image
from werkzeug.utils import secure_filename

from VisionNova.loader import Loader
from VisionNova.model import Keras_enhancer
from VisionNova.pillow import Pillow_enhancer
from VisionNova.utils import ImageUtils

app = Flask(__name__)
socketio = SocketIO(app)

# Define paths
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads")

WEIGHTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights")

app.config["UPLOAD_DIR"] = UPLOAD_DIR

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "tif"}

keras_enhancer = Keras_enhancer(WEIGHTS_DIR)
pillow_enhancer = Pillow_enhancer()

# Ensure upload and download directories exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# Function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/enhance", methods=["POST"])
def enhance_image():
    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400

    file = request.files["image"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_DIR"], filename)
        file.save(filepath)

        enhancement_type = request.form["enhancement"]
        library, enhancement_type = enhancement_type.split("_")
        factor = int(request.form.get("factor", 1))

        batch_size = 128
        enhanced_filename = "enhanced_" + filename
        output_path = os.path.join(app.config["UPLOAD_DIR"], enhanced_filename)

        try:
            # Load image
            image = Loader.load_image(filepath)
            socketio.emit("progress", {"percent": 10})
            socketio.sleep(0.1)

            if library.lower() == "pillow":
                image = Image.fromarray(image)
                socketio.emit("progress", {"percent": 30})
                socketio.sleep(0.1)

                pil_factor = 1 + (factor/100)
                image = pillow_enhancer.enhance(image, enhancement_type, pil_factor)

                socketio.emit("progress", {"percent": 80})
                socketio.sleep(0.1)

                image = np.array(image)

            else:
                processor = ImageUtils()
                image = processor.pre_process(image)
                socketio.emit("progress", {"percent": 30})
                socketio.sleep(0.1)
                
                keras_factor = max(0, min(10, factor))
                for i in range(1, keras_factor + 1):
                    image = keras_enhancer.process_image(image, batch_size, enhancement_type)
                    completion = 30 + (50 // keras_factor) * i
                    socketio.emit("progress", {"percent": completion})
                    socketio.sleep(0.1)

                image = processor.post_process(image)

            socketio.emit("progress", {"percent": 90})
            socketio.sleep(0.1)

            Loader.save_image(image, output_path)

            return send_file(output_path, mimetype="image/png")

        except Exception as e:
            return {"error": str(e)}, 500

    return {"error": "Invalid image type"}, 400


if __name__ == "__main__":
    socketio.run(app, debug=True)

import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from VisionNova.loader import Loader
from VisionNova.model import Model
from VisionNova.utils import ImageUtils

app = Flask(__name__)

# Define paths
UPLOAD_DIR = "static/uploads/"
WEIGHTS_DIR = "weights"

app.config["UPLOAD_DIR"] = UPLOAD_DIR

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

model = Model(WEIGHTS_DIR)

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
        factor = int(request.form.get("factor", 1))

        batch_size = 128

        enhanced_filename = "enhanced_" + filename
        output_path = os.path.join(app.config["UPLOAD_DIR"], enhanced_filename)

        try:
            # Load and preprocess the image
            image = Loader.load_image(filepath)
            processor = ImageUtils()
            image = processor.pre_process(image)

            # Process image
            image = model.process_image(image, batch_size, enhancement_type)

            # Postprocess and save the image
            image = processor.post_process(image)
            Loader.save_image(image, output_path)

            # Return the enhanced image as a response
            return send_file(output_path, mimetype="image/png")

        except Exception as e:
            return {"error": str(e)}, 500

    return {"error": "Invalid image type"}, 400


if __name__ == "__main__":
    app.run(debug=True)

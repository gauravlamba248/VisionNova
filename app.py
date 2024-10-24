import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from VisionNova.loader import Loader
from VisionNova.model import Model
from VisionNova.utils import ImageUtils

app = Flask(__name__)

# define paths
UPLOAD_DIR = 'static/uploads/'
WEIGHTS_DIR = os.path.abspath('weights')

app.config['UPLOAD_DIR'] = UPLOAD_DIR

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

model =  Model(WEIGHTS_DIR)

# Ensure upload and download directories exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_DIR'], filename)
        file.save(filepath)

        enhancement_type = request.form['enhancement']

        batch_size = 128

        # Create a unique filename for the enhanced image
        enhanced_filename = 'enhanced_' + filename
        output_path = os.path.join(app.config['UPLOAD_DIR'], enhanced_filename)
        
        # Set environment variable for CUDA
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        try:
            # load image and model, preprocess image
            image = Loader.load_image(filepath)
            processor = ImageUtils()
            image = processor.pre_process(image)

            # process image
            image = model.process_image(image, batch_size, enhancement_type)

            # postprocess image, save image
            image = processor.post_process(image)
            Loader.save_image(image, output_path)

            # Render the template with the enhanced image
            return render_template('index.html', enhanced_image=enhanced_filename)

        except ValueError as e:
            # Update the exception reason on the frontend if any other exception occurs
            return render_template('index.html', error=str(e))

        except Exception as e:
            # Terminate the program if a RuntimeError occurs
            print(f"Error: {e}")
            exit(1)

        # Render the template with the enhanced image
        return render_template('index.html', enhanced_image=enhanced_filename)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)

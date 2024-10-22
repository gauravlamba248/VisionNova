import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from enhancer.Enhancer import process

app = Flask(__name__)

# define paths
UPLOAD_DIR = 'static/uploads/'
WEIGHTS_DIR = 'weights'

app.config['UPLOAD_DIR'] = UPLOAD_DIR

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
        weight_path = os.path.join(WEIGHTS_DIR, enhancement_type + '.hdf5')
        image_shape = (128, 128, 3)
        batch_size = 128

        # Create a unique filename for the enhanced image
        enhanced_filename = 'enhanced_' + filename
        output_path = os.path.join(app.config['UPLOAD_DIR'], enhanced_filename)
        
        # Set environment variable for CUDA
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        # Call the process function to enhance the image
        process(weight_path, filepath, image_shape, batch_size, output_path)

        # Render the template with the enhanced image
        return render_template('index.html', enhanced_image=enhanced_filename)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
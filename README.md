# VisionNova

A Python-based image enhancer that uses deep learning techniques to restore corrupted images.

## Overview

This project provides a simple and efficient way to enhance images that have been corrupted by various types of noise or degradation. The enhancer uses deep learning models along with PIL to learn the patterns and features of the original images and then applies this knowledge to restore the corrupted images.

## Features

* Supports various types of corruption and enhancements, including:
	+ **Deep Learning Enhancements** (using Keras models):
		- Gaussian Noise
		- Grayscale
		- Black Circle
	+ **Pillow Enhancements**:
		- Sharpness
		- Color
		- Brightness
		- Contrast
* Easy-to-use interface for image enhancement
* Progress tracking for processing

## Installation

1. Clone the repository: `git clone https://github.com/nikhiljangra264/VisionNova`
1. Navigate to the project directory: `cd VisionNova`
1. Install the required packages: `pip install -r requirements.txt`

## Usage

- Run the command `python app.py`
- Upload your picture through the frontend interface.
- Select the type of enhancement from the dropdown menu.
- Specify the enhancement factor.
- Click the "Enhance" button to process the image.

## Contributing

Check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

// Function to adjust body alignment based on container height
function adjustBodyAlignment() {
    const mainContainer = document.querySelector('.main-container');
    const body = document.body;

    if (mainContainer.offsetHeight > window.innerHeight) {
        body.style.alignItems = 'flex-start'; // Align to top if container exceeds viewport
    } else {
        body.style.alignItems = 'center'; // Center if within viewport
    }
}

// Run on initial load
adjustBodyAlignment();

// Also run on window resize to check for any changes
window.addEventListener('resize', adjustBodyAlignment);

document.addEventListener('DOMContentLoaded', () => {
    // Get references to DOM elements
    const inputArea = document.getElementById('inputArea');
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const inputImage = document.getElementById('inputImage');
    const inputImageContainer = document.getElementById('inputImageContainer');
    const outputImageContainer = document.getElementById('outputImageContainer');
    const closeButton = document.getElementById('closeButton');
    const outputMessage = document.getElementById('outputMessage');
    const outputImage = document.getElementById('outputImage');
    const outputArea = document.getElementById('outputArea');
    const submitButton = document.getElementById('submitButton');
    const downloadButton = document.getElementById('downloadButton');
    const reuseButton = document.getElementById('reuseButton');
    const progressBarContainer = document.getElementById('progressBarContainer')
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');

    const socket = io();
    socket.on('connect', () => console.log("Connected to SocketIO server"));

    // Socket.IO event listeners
    socket.on('progress', function (data) {
        console.log("get progress" + data.percent);
        progressBar.value = data.percent;
        progressText.textContent = `${data.percent}%`;
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFile(files[0]);
        }
    });

    // File input click to trigger file selection
    uploadArea.addEventListener('click', () => fileInput.click());

    // Handle file input change event
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFile(file);
    });

    // Close button functionality to clear the image and reset the upload area
    closeButton.addEventListener('click', () => {
        inputImage.src = '';
        enableInput();
    });

    function showOutputImage() {
        progressBar.value = 0;
        progressBarContainer.style.display = "none";
        outputMessage.style.display = "none";
        outputImageContainer.style.display = "flex";
        outputArea.style.border = "none";
        downloadButton.style.display = "block";
        reuseButton.style.display = "block";
    }

    function hideOutputImage() {
        outputImageContainer.style.display = "none";
        downloadButton.style.display = "none";
        reuseButton.style.display = "none";
        outputMessage.style.display = "flex";
        outputArea.style.border = "2px dashed #666";
    }

    function disableInput() {
        uploadArea.style.display = "none";
        fileInput.disabled = true;
        inputImageContainer.style.display = "flex";
        inputArea.style.border = "none";
    }

    function enableInput() {
        inputArea.style.border = "2px dashed #666";
        inputImageContainer.style.display = "none";
        fileInput.value = "";
        fileInput.disabled = false;
        uploadArea.style.display = "flex";
    }

    const enhancementType = document.getElementById('enhancementType');
    const factorInput = document.getElementById('factor');

    // Managing factor range according to library used
    function updateFactorInput() {
        if (enhancementType.value.startsWith('pillow')) {
            factorInput.min = -100;
            factorInput.max = 100;
            factorInput.value = 50;
        } else {
            factorInput.min = 1;
            factorInput.max = 10;
            factorInput.value = 1;
        }
    }

    enhancementType.addEventListener('change', updateFactorInput);

    submitButton.addEventListener('click', async function () {
        const file = fileInput.files[0];
        const factor = parseFloat(factorInput.value);

        if (!file) {
            alert("Please upload an image first.");
            return;
        }
        if (enhancementType.value.startsWith('pillow')) {
            if (isNaN(factor) || factor > 100 || factor < -100) {
                alert("Please enter a valid enhancement factor between 1 and 10.");
                return;
            }
        } else if (enhancementType.value.startsWith('keras')) {
            if (isNaN(factor) || factor < 1 || factor > 10) {
                alert("Please enter a valid enhancement factor between 1 and 10.");
                return;
            }
        }

        const formData = new FormData();
        formData.append('image', file);
        formData.append('enhancement', enhancementType.value);
        formData.append('factor', factor);

        try {
            progressBarContainer.style.display = "flex";

            const response = await fetch('/enhance', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
                return;
            }

            const enhancedImageBlob = await response.blob();
            const enhancedImageUrl = URL.createObjectURL(enhancedImageBlob);

            outputImage.src = enhancedImageUrl;
            showOutputImage();
            downloadButton.href = enhancedImageUrl;
            downloadButton.download = "enhanced_image.png";
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });

    reuseButton.addEventListener('click', () => {
        // Set the enhanced image as the new original image
        inputImage.src = outputImage.src;
        // Create a new File object from the output image
        fetch(outputImage.src)
            .then(res => res.blob())
            .then(blob => {
                const file = new File([blob], "reused_image.png", { type: "image/png" });

                // Create a new FileList containing this file
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;

                disableInput();
                hideOutputImage();
            });
    });

    // Function to handle the uploaded file
    function handleFile(file) {
        if (!(file && file.type.startsWith('image/'))) {
            alert("Please upload a valid image first.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            inputImage.src = e.target.result;
            disableInput();
        };
        reader.readAsDataURL(file);
    }
});

const uploadArea = document.getElementById('uploadArea');
const imageUpload = document.getElementById('imageUpload');
const originalImage = document.getElementById('originalImage');
const outputImage = document.getElementById('outputImage');
const enhanceButton = document.getElementById('enhanceButton');
const downloadButton = document.getElementById('downloadButton');
const progressBar = document.getElementById('progressBar');
const progressValue = document.getElementById('progressValue');
const reuseButton = document.getElementById('reuseButton');

uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadArea.classList.add('active');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('active');
});

uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadArea.classList.remove('active');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        imageUpload.files = files;  // Set the dropped files to the input
        loadImage(files[0]);        // Load the image
    }
});

imageUpload.addEventListener('change', (event) => {
    loadImage(event.target.files[0]);
});

function loadImage(file) {
    const reader = new FileReader();
    reader.onload = (event) => {
        originalImage.src = event.target.result;
        originalImage.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

enhanceButton.addEventListener('click', async function() {
    const file = imageUpload.files[0];
    const enhancementType = document.getElementById('enhancementType').value;
    const factor = document.getElementById('factor').value;

    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    if (factor < 1 || factor > 10) {
        alert("Please enter a valid enhancement factor between 1 and 10.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('enhancement', enhancementType);
    formData.append('factor', factor);

    try {
        progressBar.value = 0; // Reset progress bar
        progressValue.innerText = '0%';

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
        outputImage.style.display = 'block';
        downloadButton.href = enhancedImageUrl;
        downloadButton.style.display = 'block';
        downloadButton.download = "enhanced_image.png";
        reuseButton.style.display = 'block'; 

        // Update progress bar to 100% after the process completes
        progressBar.value = 100;
        progressValue.innerText = '100%';
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});

reuseButton.addEventListener('click', () => {
    // Set the enhanced image as the new original image
    const enhancedImageUrl = outputImage.src;
    originalImage.src = enhancedImageUrl;
    originalImage.style.display = 'block';
    
    // Clear the file input
    imageUpload.value = ''; 
});

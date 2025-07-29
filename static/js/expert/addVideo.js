function previewVideo() {
    const file = document.getElementById('video_file').files[0];
    const videoPreview = document.getElementById('video_preview');
    if (file) {
        const url = URL.createObjectURL(file);
        videoPreview.src = url;
        videoPreview.style.display = "block";
    }
}

function previewThumbnail() {
    const file = document.getElementById('thumbnail').files[0];
    const thumbnailPreview = document.getElementById('thumbnail_preview');
    if (file) {
        const url = URL.createObjectURL(file);
        thumbnailPreview.src = url;
        thumbnailPreview.style.display = "block";
    }
}
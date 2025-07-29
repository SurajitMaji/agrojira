
    let currentSlide = 0;
    const images = [
        
    ]; // use correct paths

    function showSlide(index) {
        const img = document.getElementById('slider-image');
        img.src = images[index];
    }


function nextSlide() {
    currentSlide = (currentSlide + 1) % images.length;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + images.length) % images.length;
    showSlide(currentSlide);
}



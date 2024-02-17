// Update your JavaScript file (ImageGetter.js)

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/images')
        .then(response => response.json())
        .then(images => {
            const swiperContainer = document.querySelector('.swiper-wrapper');

            images.forEach((image, index) => {
                // Create a new swiper-slide for every 6 images
                if (index % 6 === 0) {
                    const swiperSlide = document.createElement('div');
                    swiperSlide.className = 'swiper-slide';

                    // Container for multiple images in a single slide
                    const imageContainer = document.createElement('div');
                    imageContainer.className = 'image-container';
                    swiperSlide.appendChild(imageContainer);

                    swiperContainer.appendChild(swiperSlide);
                }

                // Add the image to the current image container
                const currentSlide = swiperContainer.lastChild;
                const imageContainer = currentSlide.querySelector('.image-container');
                const imageUrl = '../Static/Images/lib/' + image;
                const imageElement = document.createElement('img');
                imageElement.src = imageUrl;
                imageElement.alt = 'Dish Image';
                imageContainer.appendChild(imageElement);
            });
        })
        .catch(error => console.error('Error fetching images:', error));
});

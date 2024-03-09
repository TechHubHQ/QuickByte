fetch('/api/restaurants')
  .then(response => response.json())
  .then(restaurants => {
    const container = document.getElementById('restaurant-container');

    restaurants.forEach(restaurant => {
      const card = document.createElement('div');
      card.classList.add('restaurant-card');

      card.addEventListener('click', () => {
        sessionStorage.setItem('restaurant_name', JSON.stringify(restaurant.restaurant_name));
        window.location.href = '/menu';
      });

      const image = document.createElement('img');
      if (restaurant.image_url && restaurant.image_url !== 'None') {
        // If image_url is not None, set the src to the image_url
        image.src = restaurant.image_url;
      } else {
        // If image_url is None, set the src to the default image
        image.src = '../Static/Images/IMGLib/default_restaurant.png';
      }

      image.alt = restaurant.restaurant_name;
      image.classList.add('restaurant-image');

      const details = document.createElement('div');
      details.classList.add('restaurant-details');

      const name = document.createElement('div');
      name.classList.add('restaurant-name');
      name.textContent = restaurant.restaurant_name;

      const description = document.createElement('div');
      description.classList.add('restaurant-description');
      description.textContent = restaurant.restaurant_description;

      const viewDetailsBtn = document.createElement('a');
      viewDetailsBtn.href = restaurant.web_url;
      viewDetailsBtn.textContent = 'View Details';
      viewDetailsBtn.classList.add('view-restaurant-btn');
      viewDetailsBtn.target = '_blank';

      const viewMenuBtn = document.createElement('button');
      viewMenuBtn.classList.add('view-menu-btn');
      viewMenuBtn.textContent = 'View Menu';
      viewMenuBtn.addEventListener('click', () => {
        window.location.href = '/menu';
      });

      const numberOfReviews = document.createElement('div');
      numberOfReviews.classList.add('num-reviews');
      numberOfReviews.textContent = 'Number of Reviews: ' + restaurant.number_of_reviews;

      const rating = document.createElement('div');
      rating.classList.add('restaurant-rating');
      const starCount = Math.floor(restaurant.rating);
      for (let i = 0; i < starCount; i++) {
        const star = document.createElement('span');
        star.classList.add('star');
        star.textContent = '\u2605';
        rating.appendChild(star);
      }
      if (restaurant.rating % 1 > 0) {
        const halfStar = document.createElement('span');
        halfStar.classList.add('star');
        halfStar.textContent = '\u00BD';
        rating.appendChild(halfStar);
      }

      details.appendChild(name);
      details.appendChild(description);
      details.appendChild(viewDetailsBtn);
      details.appendChild(viewMenuBtn);
      details.appendChild(numberOfReviews);
      details.appendChild(rating);

      card.appendChild(image);
      card.appendChild(details);

      container.appendChild(card);
    });
  })
  .catch(error => {
    console.error('Error fetching restaurants:', error);
  });

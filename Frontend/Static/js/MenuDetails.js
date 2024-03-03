// Fetch menu data and cuisine tabs
fetch('/api/menu')
  .then(res => res.json())
  .then(data => {
    // Get cuisine tabs container
    const cuisineTabsContainer = document.querySelector('.cuisine-tabs');

    // Get menu container
    const menuContainer = document.querySelector('.menu-items');

  // Function to create card
  const createCard = (item) => {
    // Create card
    const card = document.createElement('div');
    card.classList.add('menu-item');

    // Add item image
    const img = document.createElement('img');
    img.src = getImagePath(item.item_name.replace(/\s+/g, '_'));
    img.onerror = () => { img.src = '../../Static/Images/IMGLib/default_food.png'; }; // Set default image if the image is not found
    img.classList.add('food-img')

    // Add item details 
    const details = document.createElement('div');
    details.classList.add('item-details');

    const name = document.createElement('h3');
    name.classList.add("item-name");
    name.textContent = item.item_name;

    const description = document.createElement('p');
    description.textContent = item.item_description;

    const price = document.createElement('p');
    price.classList.add("item-price")
    price.textContent = `Price: ₹${item.item_price}`;

    const rating = document.createElement('div');
    rating.classList.add('item-rating');
    const starCount = Math.floor(item.item_rating);
    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('span');
      star.classList.add('star');
      star.textContent = '\u2605';
      rating.appendChild(star);
    }
    if (item.item_rating % 1 > 0) {
      const halfStar = document.createElement('span');
      halfStar.classList.add('star');
      halfStar.textContent = '\u00BD';
      rating.appendChild(halfStar);
    }

    const button = document.createElement('button');
    button.classList.add('add-to-cart');
    button.textContent = 'Add to Cart';

    details.appendChild(name);
    details.appendChild(description);
    details.appendChild(price);
    details.appendChild(rating);
    details.appendChild(button);

    card.appendChild(img);
    card.appendChild(details);

    // Add card to menu
    menuContainer.appendChild(card);
  };


  // Function to get image path
  const getImagePath = (itemName) => {
    const imagePath = `../Static/Images/IMGLib/${itemName}.png`;
    return imagePath;
  };


  // Function to render menu items based on cuisine
  const renderItemsByCuisine = (cuisine) => {
    // Clear menu container
    menuContainer.innerHTML = '';

    // Filter menu items by cuisine
    const filteredItems = data.filter(item => item.cuisine === cuisine || cuisine === 'All');

    // Add filtered items to menu container
    filteredItems.forEach(item => {
      createCard(item);
    });
  };

  // Function to render menu items based on filter and sort options
  const renderItemsByFilterAndSort = (filter, sort) => {
    // Clear menu container
    menuContainer.innerHTML = '';

    // Filter menu items by filter
    let filteredItems = data;
    if (filter !== 'All') {
      filteredItems = filteredItems.filter(item => item.item_category === filter);
    }

    // Sort menu items by sort
    if (sort === 'item_price') {
      filteredItems = filteredItems.sort((a, b) => a.item_price - b.item_price);
    } else if (sort === 'item_rating') {
      filteredItems = filteredItems.sort((a, b) => b.item_rating - a.item_rating);
    }

    // Add filtered and sorted items to menu container
    filteredItems.forEach(item => {
      createCard(item);
    });
  };

  // Get unique cuisines from menu data
  const cuisines = [...new Set(data.map(item => item.cuisine))];

  // Add an "All" tab
  const allTab = document.createElement('div');
  allTab.classList.add('cuisine-tab');
  allTab.textContent = 'All';
  allTab.addEventListener('click', () => {
    renderItemsByCuisine('All');
    document.querySelectorAll('.cuisine-tab').forEach(tab => tab.classList.remove('active'));
    // Add active class to the clicked tab
    allTab.classList.add('active');
  });

  // Add "All" tab to cuisine tabs container
  cuisineTabsContainer.appendChild(allTab);
  allTab.click();

  // Loop through cuisines and create tabs
  cuisines.forEach(cuisine => {
    const tab = document.createElement('div');
    tab.classList.add('cuisine-tab');
    tab.textContent = cuisine;

    tab.addEventListener('click', () => {
      renderItemsByCuisine(cuisine);
      // Remove active class from all tabs
      document.querySelectorAll('.cuisine-tab').forEach(tab => tab.classList.remove('active'));
      // Add active class to the clicked tab
      tab.classList.add('active');
    });

      cuisineTabsContainer.appendChild(tab);
  });

  // Get unique item categories from menu data
  const itemCategories = [...new Set(data.map(item => item.item_category))];

  // Create filter dropdown
  const filterSelect = document.createElement('select');
  filterSelect.addEventListener('change', () => {
    renderItemsByFilterAndSort(filterSelect.value, sortSelect.value);
  });

  // Add "All" option to filter dropdown
  const allOption = document.createElement('option');
  allOption.value = 'All';
  allOption.textContent = 'All';
  filterSelect.appendChild(allOption);

  // Add item categories to filter dropdown
  itemCategories.forEach(category => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    filterSelect.appendChild(option);
  });

  // Add filter dropdown to filter and sort container
  document.querySelector('.filter-and-sort').appendChild(filterSelect);

  // Create sort dropdown
  const sortSelect = document.createElement('select');
  sortSelect.addEventListener('change', () => {
    renderItemsByFilterAndSort(filterSelect.value, sortSelect.value);
  });

  // Add sort options to sort dropdown
  const priceOption = document.createElement('option');
  priceOption.value = 'item_price';
  priceOption.textContent = 'Sort by Price';
  sortSelect.appendChild(priceOption);

  const ratingOption = document.createElement('option');
  ratingOption.value = 'item_rating';
  ratingOption.textContent = 'Sort by Rating';
  sortSelect.appendChild(ratingOption);

  // Add sort dropdown to filter and sort container
  document.querySelector('.filter-and-sort').appendChild(sortSelect);
  });
  
  // Counter to track the number of items added to the cart
  let cartCounter = 0;

  // Function to show the "Go to Cart" box
  const showGoToCartBox = () => {
    const goToCartBox = document.querySelector('.go-to-cart-box');
    const counter = document.querySelector('.cart-counter');

    goToCartBox.style.display = 'flex';
    counter.textContent = cartCounter;
  };

  // Event listener for the "Add to Cart" button
  document.addEventListener('click', (event) => {
    if (event.target.classList.contains('add-to-cart')) {
        cartCounter++;
        showGoToCartBox();

        // Get the item details
        const item = event.target.closest('.menu-item');
        const itemName = item.querySelector('.item-name').textContent;
        const itemPrice = item.querySelector('.item-price').textContent;
        const itemImg = item.querySelector('.food-img').src;

        // Create an object to store the item details
        const cartItem = {
            name: itemName,
            price: itemPrice,
            img: itemImg,
            quantity: '1'
        };

        // Get the cart items from sessionStorage
        let cartItems = JSON.parse(sessionStorage.getItem('cartItems')) || [];

        // Check if the item is already in the cart
        const existingItem = cartItems.find(item => item.name === itemName);

        // If the item is already in the cart, update its quantity or any other property
        if (existingItem) {
            existingItem.quantity++; // For example, increment the quantity
            sessionStorage.removeItem(existingItem)
        } else {
            // If the item is not in the cart, add it
            cartItems.push(cartItem);
        }

        // Store the updated cart items in sessionStorage
        sessionStorage.setItem('cartItems', JSON.stringify(cartItems));
        console.log(sessionStorage)
    }
  });

  // Event listener for the "Go to cart" button
  document.addEventListener('click', (event) => {
    if (event.target.classList.contains("go-to-cart-btn")) {
        window.location.href = '/cart';
      }
  });

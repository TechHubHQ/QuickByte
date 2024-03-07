// Function to render items in the cart
const renderItemsInCart = () => {
    // Get the cart items from sessionStorage
    const cartItems = JSON.parse(sessionStorage.getItem('cartItems')) || [];

    // Get the container for the cart items
    const cartContainer = document.getElementById('cart-items');

    // Clear the cart container
    cartContainer.innerHTML = '';

    // If cart is empty, display a message
    if (cartItems.length === 0) {
        const img = document.createElement('img');
        img.src = '../../Static/Images/common/empty_cart.png';
        img.classList.add('empty-img')
        cartContainer.appendChild(img);
        cartContainer.appendChild(message);
        return;
    }

    // Loop through the cart items and create a card for each item
    let totalPrice = 0;
    cartItems.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('cart-item');

        const name = document.createElement('h3');
        name.textContent = item.name;

        const img = document.createElement('img');
        img.src = item.img;
        img.alt = item.name; 
        img.classList.add('item-img')// Set alt attribute for accessibility

        const price = document.createElement('p');
        const itemPrice = item.price.replace(/\D/g, '') * item.quantity;
        price.textContent = 'Price: ₹' + itemPrice; // Extract numbers from price and multiply with quantity
        totalPrice += itemPrice;

        const quantity = document.createElement('p');
        quantity.textContent = 'Quantity: ' + item.quantity;

        const plusButton = document.createElement('button');
        plusButton.classList.add('quantity-control');
        plusButton.textContent = '+';
        plusButton.addEventListener('click', () => {
            // Increase the quantity
            item.quantity++;
            // Update sessionStorage
            sessionStorage.setItem('cartItems', JSON.stringify(cartItems));
            // Re-render the items in the cart
            renderItemsInCart();
        });

        const minusButton = document.createElement('button');
        minusButton.classList.add('quantity-control');
        minusButton.textContent = '-';
        minusButton.addEventListener('click', () => {
            // Decrease the quantity
            if (item.quantity > 1) {
                item.quantity--;
            }
            // Update sessionStorage
            sessionStorage.setItem('cartItems', JSON.stringify(cartItems));
            // Re-render the items in the cart
            renderItemsInCart();
        });

        const removeButton = document.createElement('button');
        removeButton.classList.add('remove-item');
        removeButton.textContent = 'Remove';
        removeButton.addEventListener('click', () => {
            // Remove the item from sessionStorage
            const updatedCartItems = cartItems.filter(cartItem => cartItem.name !== item.name);
            sessionStorage.setItem('cartItems', JSON.stringify(updatedCartItems));
            // Re-render the items in the cart
            renderItemsInCart();
        });

        card.appendChild(name);
        card.appendChild(img); // Append the image
        card.appendChild(price);
        card.appendChild(quantity);
        card.appendChild(plusButton);
        card.appendChild(minusButton);
        card.appendChild(removeButton);

        cartContainer.appendChild(card);
    });

    // Add total payment details
    const totalPaymentDetails = document.createElement('div');
    totalPaymentDetails.classList.add('total-payment-details');
    const totalPayment = document.createElement('p');
    totalPayment.textContent = `Total Payment: ₹${totalPrice}`;
    totalPaymentDetails.appendChild(totalPayment);
    cartContainer.appendChild(totalPaymentDetails);

    if (cartItems.length > 0) {
        // Create proceed to payment button
        const proceedToPaymentButton = document.createElement('button');
        proceedToPaymentButton.classList.add('checkout-button');
        proceedToPaymentButton.textContent = 'Proceed to Payment';
        proceedToPaymentButton.addEventListener('click', () => {
            // Redirect to payment page with total payment amount as query parameter
            const totalPrice = getTotalPrice(cartItems);
            window.location.href = `/payment?total=${totalPrice}`;
        });
        
        cartContainer.appendChild(proceedToPaymentButton);
    }
};

const getTotalPrice = (cartItems) => {
    let totalPrice = 0;
    cartItems.forEach(item => {
        const itemPrice = item.price.replace(/\D/g, '') * item.quantity;
        totalPrice += itemPrice;
    });
    return totalPrice;
};


// Call the function to render items in the cart when the page loads
window.addEventListener('load', renderItemsInCart);

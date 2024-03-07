let total;

window.addEventListener('DOMContentLoaded', () => {
    const cartItems = JSON.parse(sessionStorage.getItem('cartItems')) || [];
    const paymentDetailsContainer = document.getElementById('paymentDetails');
    paymentDetailsContainer.innerHTML = '';

    let subtotal = 0;

    cartItems.forEach(item => {
        const itemTotalPrice = parseFloat(item.price.replace(/[^\d.]/g, '')) * item.quantity;
        subtotal += itemTotalPrice;

        const paymentItem = document.createElement('div');
        paymentItem.classList.add('payment-item');

        const itemName = document.createElement('span');
        itemName.textContent = item.name;

        const itemPrice = document.createElement('span');
        itemPrice.textContent = `Price: ₹${itemTotalPrice.toFixed(2)}`;

        const itemQuantity = document.createElement('span');
        itemQuantity.textContent = `Quantity: ${item.quantity}`;

        paymentItem.appendChild(itemName);
        paymentItem.appendChild(itemPrice);
        paymentItem.appendChild(itemQuantity);

        paymentDetailsContainer.appendChild(paymentItem);
    });

    // Calculate total and display
    const tax = subtotal * 0.01;
    total = subtotal + tax; // Assign total a value here

    const paymentTotal = document.createElement('div');
    paymentTotal.classList.add('payment-total');

    const subtotalSpan = document.createElement('span');
    subtotalSpan.textContent = `Subtotal: ₹${subtotal.toFixed(2)}`;

    const taxSpan = document.createElement('span');
    taxSpan.textContent = `Tax: ₹${tax.toFixed(2)}`;

    const totalSpan = document.createElement('span');
    totalSpan.classList.add('total-payment')
    totalSpan.textContent = `Total: ₹${total.toFixed(2)}`;

    paymentTotal.appendChild(subtotalSpan);
    paymentTotal.appendChild(taxSpan);
    paymentTotal.appendChild(totalSpan);

    paymentDetailsContainer.appendChild(paymentTotal);
});


function openTab(tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
}

function displayTickAnimation() {

    // Create a div element for the tick symbol
    const tickDiv = document.createElement('div');
    tickDiv.classList.add('tick-animation');

    document.body.appendChild(tickDiv);

    setTimeout(() => {
        document.body.removeChild(tickDiv);
    }, 2000); // Adjust the delay as needed
}

function displayCrossAnimation() {
    // Clear all contents in the payment details container
    clearPaymentDetails();

    // Create a div element for the cross symbol
    const crossDiv = document.createElement('div');
    crossDiv.classList.add('cross-animation');

    // Append the cross symbol div to the document body
    document.body.appendChild(crossDiv);

    // After a delay, remove the cross symbol from the document
    setTimeout(() => {
        document.body.removeChild(crossDiv);
    }, 2000); // Adjust the delay as needed
}

// Function to handle UPI payment form submission
function payViaUPI(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the UPI ID entered by the user
    const upiId = document.getElementById('upi-id').value;
    const paidAmount = total; // Access total value
    console.log('UPI ID:', upiId);
    console.log('paid amount:', paidAmount);

    // Send the UPI ID to the backend API
    fetch("/pay_via_upi", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            payment_type: 'UPI',
            upi_id: upiId,
            paid_amount: paidAmount
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('UPI payment successful');
            displayTickAnimation(); // Display tick symbol animation on success
            // Optionally, display a success message or perform other actions
        } else {
            console.error('UPI payment failed');
            displayCrossAnimation()
        }
    })
    .catch(error => {
        console.error('Error processing UPI payment:', error);
        displayCrossAnimation()
    });
}

// Function to handle card payment form submission
function payViaCard(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the card details entered by the user
    const cardNumber = document.getElementById('card-number').value;
    const cardholderName = document.getElementById('cardholder-name').value;
    const expirationDate = document.getElementById('expiration-date').value;
    const cvv = document.getElementById('cvv').value;
    const paidAmount = total; // Access total value
    console.log('paid amount:', paidAmount);

    // Send the card details to the backend API
    fetch('/pay_via_card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            payment_type: 'CARD',
            card_number: cardNumber,
            cardholder_name: cardholderName,
            expiration_date: expirationDate,
            cvv: cvv,
            paid_amount: paidAmount
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('Card payment successful');
            displayTickAnimation(); // Display tick symbol animation on success
        } else {
            console.error('Card payment failed');
            displayCrossAnimation()
        }
    })
    .catch(error => {
        console.error('Error processing card payment:', error);
        displayCrossAnimation()
    });
}

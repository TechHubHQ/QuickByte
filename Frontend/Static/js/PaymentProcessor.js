let total;

window.addEventListener('DOMContentLoaded', () => {
    const paymentMade = sessionStorage.getItem('paymentMade');

    if (paymentMade === 'true') {
        // disablePaymentOptions();
    } else {
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

        const tax = subtotal * 0.01;
        const total = subtotal + tax;

        const paymentTotal = document.createElement('div');
        paymentTotal.classList.add('payment-total');

        const subtotalSpan = document.createElement('span');
        subtotalSpan.textContent = `Subtotal: ₹${subtotal.toFixed(2)}`;

        const taxSpan = document.createElement('span');
        taxSpan.textContent = `Tax: ₹${tax.toFixed(2)}`;

        const totalSpan = document.createElement('span');
        totalSpan.classList.add('total-payment');
        totalSpan.textContent = `Total: ₹${total.toFixed(2)}`;

        paymentTotal.appendChild(subtotalSpan);
        paymentTotal.appendChild(taxSpan);
        paymentTotal.appendChild(totalSpan);

        paymentDetailsContainer.appendChild(paymentTotal);

        const priceDetails = {
            subtotal: subtotal.toFixed(2),
            tax: tax.toFixed(2),
            total: total.toFixed(2)
        };

        sessionStorage.setItem('priceDetails', JSON.stringify(priceDetails));
    }
});

function disablePaymentOptions() {
    document.getElementById('upi-form').style.display = 'none';
    document.getElementById('card-form').style.display = 'none';
    const paymentOptionsContainer = document.getElementById('payment-options');
    if (!paymentOptionsContainer) {
        console.error('Payment options container not found');
        return;
    }
    const paymentMessage = document.createElement('div');
    paymentMessage.textContent = 'Payment has already been made for this order.';
    document.getElementsByClassName('payment-container').appendChild(paymentMessage);
}

function payViaUPI(event) {
    event.preventDefault(); 
    const paymentMade = sessionStorage.getItem('paymentMade');
    if (paymentMade === 'true') {
        console.log('Payment has already been made for this order.');
        return;
    }
    
    const upiId = document.getElementById('upi-id').value;
    const priceDetailsString = sessionStorage.getItem('priceDetails');
    const priceDetails = JSON.parse(priceDetailsString);
    const paidAmount = parseFloat(priceDetails.total);

    console.log('UPI ID:', upiId);
    console.log('paid amount:', paidAmount);

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
            displayTickAnimation();
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

function payViaCard(event) {
    event.preventDefault(); 

    const paymentMade = sessionStorage.getItem('paymentMade');
    if (paymentMade === 'true') {
        console.log('Payment has already been made for this order.');
        return;
    }

    const cardNumber = document.getElementById('card-number').value;
    const cardholderName = document.getElementById('cardholder-name').value;
    const expirationDate = document.getElementById('expiration-date').value;
    const cvv = document.getElementById('cvv').value;
    const paidAmount = parseFloat(sessionStorage.getItem('priceDetails').total);
    console.log('paid amount:', paidAmount);

 
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
            displayTickAnimation();
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


function openTab(tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
}

function displayTickAnimation() {

    while (document.body.firstChild) {
        document.body.removeChild(document.body.firstChild);
    }

    const tickDiv = document.createElement('div');
    tickDiv.classList.add('tick-animation');
    document.body.appendChild(tickDiv);

    const successMessage = document.createElement('div');
    successMessage.textContent = 'Order Placed Successfully';
    successMessage.classList.add('success-message');
    document.body.appendChild(successMessage);
    document.body.classList.add('success-background');
    sessionStorage.setItem('paymentMade', true)

    setTimeout(() => {
        window.location.href = '/order_tracker';
    }, 1000);
}

function displayCrossAnimation() {

    const crossDiv = document.createElement('div');
    crossDiv.classList.add('cross-animation');

    document.body.appendChild(crossDiv);
    setTimeout(() => {
        document.body.removeChild(crossDiv);
    }, 1000);

    setTimeout(() => {
        window.location.href = '/landing';
    }, 1000);
}
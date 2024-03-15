function sendDataToBackend(data) {
  fetch('/place_order', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => {
      if (response.ok) {
          console.log('Data sent successfully');
          sessionStorage.setItem('orderSent', 'true');
          fetchOrderDetails();
      } else {
          console.error('Error sending data');
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

function showLoader() {
  document.getElementById('loader').style.display = 'block';
}

function hideLoader() {
  document.getElementById('loader').style.display = 'none';
}

function fetchOrderDetails() {
  showLoader();
  fetch('/get_order_details')
  .then(response => {
      if (response.ok) {
          return response.json();
      } else {
          throw new Error('Failed to fetch order details');
      }
  })
  .then(data => {
      hideLoader();
      document.getElementById('order-no').textContent = data.order_id;
      document.getElementById('order-status').textContent = data.order_status;
      document.getElementById('delivery-address').textContent = data.delivery_address;

      const progressSteps = document.querySelectorAll('.progress-step');
      const completedSteps = data.completed_steps;

      progressSteps.forEach((step, index) => {
          const stepLabel = step.querySelector('.step-label').textContent;
          if (stepLabel === data.order_status) {
              step.classList.add('active');
              step.querySelector('.step-label').classList.add('active-label'); 
          } else {
              step.classList.remove('active');
              step.querySelector('.step-label').classList.remove('active-label');
          }
          if (completedSteps.includes(stepLabel)) {
              step.classList.add('completed');
          } else {
              step.classList.remove('completed');
          }
      });
  })
  .catch(error => {
      hideLoader();
      console.error('Error fetching order details:', error);
  });
}

function extractDataFromSessionStorage() {
  const cartItemsString = sessionStorage.getItem('cartItems');
  const restaurantName = sessionStorage.getItem('restaurant_name');
  const priceDetailsString = sessionStorage.getItem('priceDetails');

  let cartItems = [];
  let priceDetails = null;
  let subtotal = 0;
  let tax = 0;
  let total = 0;

  if (cartItemsString) {
      cartItems = JSON.parse(cartItemsString);
  }

  if (priceDetailsString) {
      priceDetails = JSON.parse(priceDetailsString);
      ({ subtotal, tax, total } = priceDetails);
  }

  const orderItems = cartItems.map(item => ({
      name: item.name,
      price: item.price,
      img: item.img,
      quantity: item.quantity
  }));

  const orderDetails = {
      restaurantName: restaurantName,
      orderAmount: total,
      orderTax: tax,
      subtotal: subtotal,
      items: orderItems
  };

  console.log(orderDetails)

  return orderDetails;
}

function sendOrderDetailsOnPageLoad() {
  const orderSent = sessionStorage.getItem('orderSent');
  if (!orderSent) { 
      const orderDetails = extractDataFromSessionStorage();
      sendDataToBackend(orderDetails);
  }
}

function cancelOrder() {
  const orderNo = document.getElementById('order-no').textContent
  const orderStatus = document.getElementById('order-status').textContent;
  const cancelMessage = document.getElementById('cancel-message');

  if (orderStatus === 'Out for Delivery' || orderStatus === 'Delivered') {
    cancelMessage.textContent = 'Cannot cancel the order in this stage.';
    cancelMessage.style.display = 'block';
    setTimeout(() => {
      cancelMessage.style.display = 'none';
    }, 2000);
    return;
  }

  fetch('/cancel_order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ order_id: orderNo })
  })
  .then(response => {
    if (response.ok) {
      console.log('Order Cancelled successfully');

    } else {
      console.error('Error cancelling order');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

window.onload = () => {
  sendOrderDetailsOnPageLoad();
  setTimeout(() => {
    fetchOrderDetails();
  }, 3000);
};

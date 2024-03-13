window.addEventListener('DOMContentLoaded', () => {
    fetch("/my_orders_data")
        .then(response => response.json())
        .then(data => {
            const ordersContainer = document.getElementById('orders-container');
            ordersContainer.innerHTML = '';

            data.forEach(order => {
                const orderBox = document.createElement('div');
                orderBox.classList.add('order-box');

                const orderId = document.createElement('h3');
                orderId.className = "order-id";
                orderId.textContent = `Order ID: ${order.order_id}`;

                const orderStatus = document.createElement('p');
                orderStatus.textContent = `Status: ${order.order_status}`;

                const trackOrderBtn = document.createElement('button');
                trackOrderBtn.textContent = "OrderStatusTracker";
                trackOrderBtn.classList.add('track-order-btn');
                trackOrderBtn.addEventListener('click', () => trackOrder(order.order_id));

                orderBox.appendChild(orderId);
                orderBox.appendChild(orderStatus);
                orderBox.appendChild(trackOrderBtn);

                ordersContainer.appendChild(orderBox);
            });
        })
        .catch(error => {
            console.error('Error fetching orders:', error);
        });
});

function displayOrderTracker(orderdata) {
    const orderBox = document.querySelector(".orders-container");
    orderBox.style.display = "none";
    const orderTrackerWidget = document.querySelector(".order-tracker-widget");
    orderTrackerWidget.style.display = "flex";
    document.getElementById("order-no").textContent = orderdata.order_id;
    document.getElementById("order-status").textContent = orderdata.order_status;
    document.getElementById("delivery-address").textContent = orderdata.delivery_address;

    console.log(orderdata.order_status);

    if (orderdata.order_status == 'Order Cancelled') {
        const orderPlaced = document.getElementById("order-placed");
        orderPlaced.classList.add("completed")
        const orderConfirmed = document.getElementById("order-confirmed")
        orderConfirmed.style.display = "none";
        const orderPrepared = document.getElementById("order-prepared");
        orderPrepared.style.display = "none";
        const orderReady = document.getElementById("order-ready");
        orderReady.style.display = "none";
        const capAssigned = document.getElementById("cap-assigned");
        capAssigned.style.display = "none";
        const outForDelv = document.getElementById("out-for-delv");
        outForDelv.style.display = "none";
        const delivery = document.getElementById("delivered");
        delivery.style.display = "none";
        const orderCanceled = document.getElementById("order-cancelled");
        orderCanceled.style.display = "flex";
    }
    
    else {
        const progressSteps = document.querySelectorAll('.progress-step');
        const completedSteps = orderdata.completed_steps;

        progressSteps.forEach((step, index) => {
            const stepLabel = step.querySelector('.step-label').textContent;
            if (stepLabel === orderdata.order_status) {
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
        })
    };
}

function cancelOrder() {
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
      body: JSON.stringify({ order_id: orderId })
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

  function trackOrder(orderId) {
    console.log(orderId);
    fetch('/order_status_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            order_id: orderId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error fetching order status:', data.error);
            return;
        }
        console.log(data);
        displayOrderTracker(data);
        // Replace the heading text
        document.querySelector('.my-orders').textContent = 'Order Status Tracker';
    })
    .catch(error => {
        console.error('Error fetching order status:', error);
    });
}

function BackToOrders() {
    const orderTrackerWidget = document.querySelector('.order-tracker-widget');
    orderTrackerWidget.style.display = 'none';
    const ordersContainer = document.querySelector(".orders-container");
    ordersContainer.style.display = "flex";
}

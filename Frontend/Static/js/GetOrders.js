fetch('/my_orders_data')
    .then(response => response.json())
    .then(data => {
        const orderContainer = document.getElementById('order-container');
        const orderDetailsWidget = document.getElementById('order-details-widget');

        data.forEach(order => {
            const orderBox = document.createElement('div');
            orderBox.classList.add('order-box');

            const orderId = document.createElement('div');
            orderId.classList.add('order-id');
            orderId.textContent = `Order ID: ${order.order_id}`;
            orderBox.appendChild(orderId);

            const orderTotal = document.createElement('div');
            orderTotal.classList.add('order-total');
            orderTotal.textContent = `Total: ₹${order.order_amount}`;
            orderBox.appendChild(orderTotal);

            const itemsList = document.createElement('ul');
            order.items.forEach(item => {
                const itemElement = document.createElement('li');
                itemElement.textContent = `${item.item_name} (${item.item_quantity})`;
                itemsList.appendChild(itemElement);
            });
            orderBox.appendChild(itemsList);

            orderBox.addEventListener('click', () => {
                showOrderDetails(order);
                orderDetailsWidget.style.display = 'block';
                orderContainer.style.display = 'none';
            });

            orderContainer.appendChild(orderBox);
        });

        function showOrderDetails(order) {
            orderDetailsWidget.innerHTML = '';

            const orderDetailsHeader = document.createElement('div');
            orderDetailsHeader.className = 'order-details-header';
            orderDetailsHeader.innerHTML = `
                <h2>Order Details</h2>
                <p>Order ID: ${order.order_id}</p>
                <p>Restaurant: ${order.restaurant_name}</p>
                <p>Order Status: ${order.order_status}</p>
                <p>Order Type: ${order.order_type}</p>
            `;
            orderDetailsWidget.appendChild(orderDetailsHeader);

            const orderDetailsTable = document.createElement('table');
            orderDetailsTable.className = 'order-details-table';
            orderDetailsTable.innerHTML = `
                <tr>
                    <th>Detail</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Order Base Price</td>
                    <td>₹${order.order_base_price}</td>
                </tr>
                <tr>
                    <td>Order Tax</td>
                    <td>₹${order.order_tax}</td>
                </tr>
                <tr>
                    <td>Order Amount</td>
                    <td>₹${order.order_amount}</td>
                </tr>
                <tr>
                    <td>Delivery To</td>
                    <td>${order.delivery_to}</td>
                </tr>
                <tr>
                    <td>Delivery Address</td>
                    <td>${order.delivery_addr}</td>
                </tr>
            `;
            orderDetailsWidget.appendChild(orderDetailsTable);

            const orderItemsTable = document.createElement('table');
            orderItemsTable.className = 'order-items-table';
            orderItemsTable.innerHTML = `
                <tr>
                    <th>Item No.</th>
                    <th>Item Name</th>
                    <th>Price</th>
                    <th>Quantity</th>
                </tr>
            `;
            order.items.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.item_no}</td>
                    <td>${item.item_name}</td>
                    <td>₹${item.item_price}</td>
                    <td>${item.item_quantity}</td>
                `;
                orderItemsTable.appendChild(row);
            });
            orderDetailsWidget.appendChild(orderItemsTable);

            const backButton = document.createElement('button');
            backButton.classList.add('back-button')
            backButton.textContent = 'Back';
            backButton.addEventListener('click', () => {
                orderDetailsWidget.style.display = 'none';
                orderContainer.style.display = 'flex';
            });
            orderDetailsWidget.appendChild(backButton);
        }
    })
    .catch(error => console.error('Error:', error));

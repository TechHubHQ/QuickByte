import os
import time
import sys

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from datetime import datetime
from app import app
from Backend.Models.QBmOrder2ItemModel import OrderDetailsHeader, UpdateOrderStatus, UpdateOrderStatusTimeStamps

# Push the app context
app.app_context().push()

# Define order status mapping
ORDER_STATUS_MAPPING = {
    'Order Placed': 'Order Confirmed',
    'Order Confirmed': 'Preparing Order',
    'Preparing Order': 'Order Ready',
    'Order Ready': 'Captain Assigned',
    'Captain Assigned': 'Out for Delivery',
    'Out for Delivery': 'Delivered'
}


def update_order_status():
    while True:
        try:
            # Query orders that need status update
            orders = OrderDetailsHeader.query.filter(
                OrderDetailsHeader.order_status.in_(ORDER_STATUS_MAPPING.keys()),
                OrderDetailsHeader.order_cancel_time.is_(None),
                OrderDetailsHeader.order_delivered_time.is_(None)
            ).all()

            # Process orders if found
            if orders:
                for order in orders:
                    current_status = order.order_status
                    next_status = ORDER_STATUS_MAPPING.get(current_status)
                    if next_status:
                        UpdateOrderStatus(order.order_id, next_status)
                        UpdateOrderStatusTimeStamps(order.order_id, next_status)
                        print(
                            f"{datetime.now()} - Order {order.order_id} updated from '{current_status}' to '{next_status}'")
            else:
                print(f"{datetime.now()} - No orders found requiring status update")
                # Print alive ping
                print(f"{datetime.now()} -- OrderStatusEngine is alive -- Process ID: {os.getpid()}")

            # Sleep for 2 minutes
            time.sleep(120)

        except Exception as e:
            # Log any errors and continue
            print(f"Error occurred: {e}")
            time.sleep(60)  # Wait for a minute before retrying in case of error


if __name__ == '__main__':
    update_order_status()

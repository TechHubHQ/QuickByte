import os
import time
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
# Ensure the directory for logs exists
LOGIC_LOG_DIR = os.environ.get("LOGIC_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=os.path.join(LOGIC_LOG_DIR, f'{current_date}_OrderStatusEngine.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from Backend.Models.QBmOrder2ItemModel import OrderDetailsHeader, UpdateOrderStatus, UpdateOrderStatusTimeStamps

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


def OrderStatusEngine():
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
                        logging.info(
                            f"Order {order.order_id} updated from '{current_status}' to '{next_status}'")
            else:
                logging.info("No orders found requiring status update")
                # Print alive ping
                logging.info(f"OrderStatusEngine is alive -- Process ID: {os.getpid()}")

            # Sleep for 2 minutes
            time.sleep(120)

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(60)  # Wait for a minute before retrying in case of error


if __name__ == '__main__':
    OrderStatusEngine()

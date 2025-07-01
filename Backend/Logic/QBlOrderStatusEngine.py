# ===============================================================================================================
# This script is an Order Status Engine that runs continuously and updates the status of orders
# in a database based on a predefined order status mapping. Here's a breakdown of the main functionality:

# 1. Imports necessary modules and sets up logging.
# 2. Configures the application context for the Flask app.
# 3. Defines an ORDER_STATUS_MAPPING dictionary that maps the current order status to the next status.
# 4. The OrderStatusEngine function:
#   a. Queries the database for orders that need a status update based on the order status and order
#      cancellation/delivery status.
#   b. For each order found, it updates the order status to the next status in the mapping using the
#      UpdateOrderStatus and UpdateOrderStatusTimeStamps functions.
#   c. Logs the status update for each order.
#   d. If no orders are found, it logs a message indicating that no orders require a status update.
#   e. Logs an "alive ping" message with the process ID.
#   f. Sleeps for 2 minutes before running the loop again.
# 5. Catches and logs any exceptions that occur during execution and waits for 1 minute before retrying.
# 6. The main function calls OrderStatusEngine when the script is run directly.

# This script is designed to be run continuously, either as a standalone script or as part of a larger application,
# to maintain the order status in the database based on the predefined order status flow.
# =====================================================================================================================


# ===========================================================
# Imports/Packages
# ===========================================================

from Config.PyLogger import RollingFileHandler
from Backend.Models.QBmOrder2ItemModel import OrderDetailsHeader, UpdateOrderStatus, UpdateOrderStatusTimeStamps
from app import app
import os
import time
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
INTEGRATION_LOG_DIR = os.environ.get("LOGIC_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RollingFileHandler(INTEGRATION_LOG_DIR, 'OrderStatusEngine.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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

# ======================================================================
# OrderStatusEngine to update the status of the orders from DB
# =======================================================================


def OrderStatusEngine():
    """
    This function runs in an infinite loop and performs the following tasks:

    1. Queries the database for orders that need a status update based on the following conditions:
        - The order status is one of the keys in the ORDER_STATUS_MAPPING dictionary.
        - The order has not been canceled (order_cancel_time is None).
        - The order has not been delivered (order_delivered_time is None).

    2. If there are orders found, it processes each order as follows:
        - Retrieves the current order status.
        - Looks up the next status in the ORDER_STATUS_MAPPING dictionary using the current status.
        - If a next status is found, it calls the UpdateOrderStatus and UpdateOrderStatusTimeStamps functions
          to update the order status and timestamps in the database.
        - Logs a message indicating the order ID and the status change.

    3. If no orders are found, it logs a message indicating that no orders require a status update.
    4. Logs an "alive ping" message with the current process ID to indicate that the script is running.
    5. Sleeps for 2 minutes (120 seconds) before repeating the loop.

    If an exception occurs during execution, it logs the error message and waits for 1 minute (60 seconds)
    before retrying the loop.

    This function is designed to run continuously, as a standalone script,
    to maintain the order status in the database based on the predefined order status flow.
    """

    while True:
        try:
            # Query orders that need status update
            orders = OrderDetailsHeader.query.filter(
                OrderDetailsHeader.order_status.in_(
                    ORDER_STATUS_MAPPING.keys()),
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
                        UpdateOrderStatusTimeStamps(
                            order.order_id, next_status)
                        logging.info(
                            f"Order {order.order_id} updated from '{current_status}' to '{next_status}'")
            else:
                logging.info("No orders found requiring status update")
                # Print alive ping
                logging.info(
                    f"OrderStatusEngine is alive -- Process ID: {os.getpid()}")

            # Sleep for 2 minutes
            time.sleep(120)

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            # Wait for a minute before retrying in case of error
            time.sleep(60)
            logging.info(
                f"OrderStatusEngine Waiting to restart after error -- Process ID: {os.getpid()}")


if __name__ == '__main__':
    OrderStatusEngine()

# ====================================================================================================================
# This module provides functionality for generating unique order IDs and creating order header and order item records
# in the database.

# It includes the following components:

# 1. The `generate_order_id` function generates a unique order ID based on the current date and random characters.
#    It checks if the generated order ID already exists in the database, and if so, it generates a new one.

# 2. The `HandleOrderGeneration` class encapsulates methods for creating order header and order item records.

#    - The `OrderHeaderCreation` static method creates an order header record in the database with the provided
#      information, such as user details, order details, and delivery information.

#    - The `OrderItemCreation` static method creates an order item record in the database with the provided
#      information, such as order ID, item details, and quantity.

# Both the function and class methods handle exceptions and log any errors that occur during execution.
# ===================================================================================================================


# =======================================================
# Imports/Packages
# =======================================================

import string
import random
from datetime import datetime
import logging
from Backend.Models.QBmOrder2ItemModel import CreateOrderHeader, CreateOrderItem, CheckOrder


# =======================================================
# generate_order_id -- generates an unique order ID
# =======================================================
def generate_order_id():
    """
    Generates a unique order ID based on the current date and random characters.

    Returns:
        str: A unique order ID in the format "YYYYMMDDXXXX" where "XXXX" is a random 4-character string.

    If an exception occurs during order ID generation, it logs the error message.
    """
    try:
        current_date = datetime.now().strftime("%Y%m%d")
        random_uid = ''.join(random.choices(string.ascii_uppercase, k=4))
        order_id = f"{current_date}{random_uid}"
        if CheckOrder(order_id=order_id):
            return order_id
        else:
            generate_order_id()
    except Exception as e:
        logging.error(f"Error generating order ID: {e}")


# =====================================================================
# HandleOrderGeneration -- class for handling order generation
# =====================================================================

class HandleOrderGeneration:
    """
    This class provides static methods for creating order header and order item records in the database.
    """
    @staticmethod
    def OrderHeaderCreation(
        username,
        order_id,
        restaurant_name,
        order_status,
        order_type,
        order_base_price,
        order_tax,
        order_amount,
        order_rcv_time,
        order_accept_time,
        order_prep_time,
        order_ready_time,
        captain_assigned_time,
        out_for_delivery_time,
        order_delivered_time,
        order_cancel_time,
        delivery_to,
        delivery_addr,
    ):
        
        """
        Creates an order header record in the database with the provided information.

        Args:
            username (str): The username of the user placing the order.
            order_id (str): The unique order ID.
            restaurant_name (str): The name of the restaurant where the order is placed.
            order_status (str): The current status of the order.
            order_type (str): The type of order (e.g., delivery, pickup).
            order_base_price (float): The base price of the order.
            order_tax (float): The tax amount for the order.
            order_amount (float): The total amount of the order.
            order_rcv_time (datetime): The time when the order was received.
            order_accept_time (datetime): The time when the order was accepted.
            order_prep_time (datetime): The time when order preparation started.
            order_ready_time (datetime): The time when the order was ready for delivery/pickup.
            captain_assigned_time (datetime): The time when a captain was assigned for delivery.
            out_for_delivery_time (datetime): The time when the order was out for delivery.
            order_delivered_time (datetime): The time when the order was delivered.
            order_cancel_time (datetime): The time when the order was canceled (if applicable).
            delivery_to (str): The name of the person/location where the order is to be delivered.
            delivery_addr (str): The delivery address.

        Returns:
            The created order header record.

        If an exception occurs during order header creation, it logs the error message.
        """
         
        try:
            order_header = CreateOrderHeader(
                user_name=username,
                order_id=order_id,
                restaurant_name=restaurant_name,
                order_status=order_status,
                order_type=order_type,
                order_base_price=order_base_price,
                order_tax=order_tax,
                order_amount=order_amount,
                order_rcv_time=order_rcv_time,
                order_accept_time=order_accept_time,
                order_prep_time=order_prep_time,
                order_ready_time=order_ready_time,
                captain_assigned_time=captain_assigned_time,
                out_for_delivery_time=out_for_delivery_time,
                order_delivered_time=order_delivered_time,
                order_cancel_time=order_cancel_time,
                delivery_to=delivery_to,
                delivery_addr=delivery_addr,
            )
            return order_header
        except Exception as e:
            logging.error(f"Error creating order header: {e}")

    @staticmethod
    def OrderItemCreation(order_id, item_no, item_name, item_price, item_quantity):
        """
        Creates an order item record in the database with the provided information.

        Args:
            order_id (str): The unique order ID.
            item_no (int): The item number/identifier.
            item_name (str): The name of the item.
            item_price (float): The price of the item.
            item_quantity (int): The quantity of the item ordered.

        Returns:
            The created order item record.

        If an exception occurs during order item creation, it logs the error message.
        """
        
        try:
            order_item = CreateOrderItem(
                order_id=order_id,
                item_no=item_no,
                item_name=item_name,
                item_price=item_price,
                item_quantity=item_quantity
            )
            return order_item
        except Exception as e:
            logging.error(f"Error creating order item: {e}")

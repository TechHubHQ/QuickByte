import string
import random
from datetime import datetime
import logging
from Backend.Models.QBmOrder2ItemModel import CreateOrderHeader, CreateOrderItem, CheckOrder


def generate_order_id():
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


class HandleOrderGeneration:
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

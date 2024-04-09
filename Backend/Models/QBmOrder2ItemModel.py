# ====================================================================================================
# Module for defining OrderDetailsHeader and OrderItemDetails classes, and related functions.

# This module contains the definition of the OrderDetailsHeader and OrderItemDetails classes,
# which represent order details and order item details in the database. It also includes functions
# for creating, updating, and checking order information in the database.

# ====================================================================================================


# ==============================================================
# Imports/Packages
# ==============================================================
from datetime import datetime
from Backend.Connections.QBcDBConnector import db


# ==================================================================
# OrderDetailsHeader table database schema
# ==================================================================
class OrderDetailsHeader(db.Model):
    """
    Model class for representing order details in the database.

    Attributes:
        id (int): The primary key ID of the order.
        user_name (str): The username associated with the order.
        order_id (str): The ID of the order.
        restaurant_name (str): The name of the restaurant associated with the order.
        order_status (str): The status of the order.
        order_type (str): The type of the order.
        order_base_price (float): The base price of the order.
        order_tax (float): The tax amount of the order.
        order_amount (float): The total amount of the order.
        order_rcv_time (datetime): The receive time of the order.
        order_accept_time (datetime): The accept time of the order.
        order_prep_time (datetime): The preparation time of the order.
        order_ready_time (datetime): The ready time of the order.
        captain_assigned_time (datetime): The time when a captain is assigned for delivery.
        out_for_delivery_time (datetime): The time when the order is out for delivery.
        order_delivered_time (datetime): The time when the order is delivered.
        order_cancel_time (datetime): The time when the order is cancelled.
        delivery_to (str): The recipient of the order.
        delivery_addr (str): The delivery address of the order.
    """
    
    __tablename__ = 'order_header'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    order_id = db.Column(db.String(50))
    restaurant_name = db.Column(db.String(50))
    order_status = db.Column(db.String(50))
    order_type = db.Column(db.String(50))
    order_base_price = db.Column(db.Float)
    order_tax = db.Column(db.Float)
    order_amount = db.Column(db.Float)
    order_rcv_time = db.Column(db.DateTime)
    order_accept_time = db.Column(db.DateTime)
    order_prep_time = db.Column(db.DateTime)
    order_ready_time = db.Column(db.DateTime)
    captain_assigned_time = db.Column(db.DateTime)
    out_for_delivery_time = db.Column(db.DateTime)
    order_delivered_time = db.Column(db.DateTime)
    order_cancel_time = db.Column(db.DateTime)
    delivery_to = db.Column(db.String(50))
    delivery_addr = db.Column(db.String(50))


# =====================================================================
# OrderItemDetails table database schema
# =====================================================================
class OrderItemDetails(db.Model):
    """
    Model class for representing order item details in the database.

    Attributes:
        id (int): The primary key ID of the order item.
        item_no (int): The item number of the order item.
        order_id (str): The ID of the order associated with the order item.
        item_name (str): The name of the order item.
        item_price (float): The price of the order item.
        item_quantity (int): The quantity of the order item.
    """
    
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    item_no = db.Column(db.Integer)
    order_id = db.Column(db.String(50))
    item_name = db.Column(db.String(50))
    item_price = db.Column(db.Float)
    item_quantity = db.Column(db.Integer)


# ===================================================================================
# CreateOrderHeader() --> Create a new order header record in the database.
# ===================================================================================
def CreateOrderHeader(
    user_name,
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
    delivery_addr
):
    """
    Creates a new order header entry in the database.

    Args:
        user_name (str): The username associated with the order.
        order_id (str): The ID of the order.
        restaurant_name (str): The name of the restaurant associated with the order.
        order_status (str): The status of the order.
        order_type (str): The type of the order.
        order_base_price (float): The base price of the order.
        order_tax (float): The tax amount of the order.
        order_amount (float): The total amount of the order.
        order_rcv_time (datetime): The receive time of the order.
        order_accept_time (datetime): The accept time of the order.
        order_prep_time (datetime): The preparation time of the order.
        order_ready_time (datetime): The ready time of the order.
        captain_assigned_time (datetime): The time when a captain is assigned for delivery.
        out_for_delivery_time (datetime): The time when the order is out for delivery.
        order_delivered_time (datetime): The time when the order is delivered.
        order_cancel_time (datetime): The time when the order is cancelled.
        delivery_to (str): The recipient of the order.
        delivery_addr (str): The delivery address of the order.

    Returns:
        OrderDetailsHeader: The created order header entry.
    """
    
    order_header = OrderDetailsHeader(
        user_name=user_name,
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
        delivery_addr=delivery_addr
    )
    db.session.add(order_header)
    db.session.commit()
    return order_header


# =========================================================================================
# CreateOrderItem() --> Create a new order item record in the database.
# =========================================================================================
def CreateOrderItem(
    order_id,
    item_no,
    item_name,
    item_price,
    item_quantity
):
    """
    Creates a new order item entry in the database.

    Args:
        order_id (str): The ID of the order associated with the order item.
        item_no (int): The item number of the order item.
        item_name (str): The name of the order item.
        item_price (float): The price of the order item.
        item_quantity (int): The quantity of the order item.

    Returns:
        OrderItemDetails: The created order item entry.
    """
    
    order_item = OrderItemDetails(
        order_id=order_id,
        item_no=item_no,
        item_name=item_name,
        item_price=item_price,
        item_quantity=item_quantity,
    )
    db.session.add(order_item)
    db.session.commit()
    return order_item


# ============================================================================= 
# UpdateOrderStatus() --> Update the status of an order in the database.
# =============================================================================
def UpdateOrderStatus(order_id, order_status):
    """
    Updates the status of an order in the database.

    Args:
        order_id (str): The ID of the order to update.
        order_status (str): The new status of the order.

    Returns:
        str: The updated order status.
    """
    
    order = OrderDetailsHeader.query.filter_by(order_id=order_id).first()
    order.order_status = order_status
    db.session.commit()
    return order.order_status


# =====================================================================================
# UpdateOrderStatusTimeStamps() --> Update the timestamps of an order in the database.
# =====================================================================================
def UpdateOrderStatusTimeStamps(order_id, order_status):
    """
    Updates the status and corresponding timestamps of an order in the database.

    Args:
        order_id (str): The ID of the order to update.
        order_status (str): The new status of the order.

    Returns:
        OrderDetailsHeader: The updated order entry.
    """
    
    order = OrderDetailsHeader.query.filter_by(order_id=order_id).first()
    order.order_status = order_status
    if order_status == 'Order Cancelled':
        order.order_cancel_time = datetime.now()
    elif order_status == 'Delivered':
        order.order_delivered_time = datetime.now()
    elif order_status == 'Out for Delivery':
        order.out_for_delivery_time = datetime.now()
    elif order_status == 'Captain Assigned':
        order.captain_assigned_time = datetime.now()
    elif order_status == 'Order Ready':
        order.order_ready_time = datetime.now()
    elif order_status == 'Preparing Order':
        order.order_prep_time = datetime.now()
    elif order_status == 'Order Confirmed':
        order.order_accept_time = datetime.now()
    db.session.commit()
    return order


# ===================================================================================
# CheckOrder() --> Check if an order exists in the database.
# ===================================================================================
def CheckOrder(order_id):
    """
    Checks if an order with the given ID exists in the database.

    Args:
        order_id (str): The ID of the order to check.

    Returns:
        bool: True if the order exists, False otherwise.
    """
    
    order = OrderDetailsHeader.query.filter_by(order_id=order_id).first()
    if not order:
        return True
    return False

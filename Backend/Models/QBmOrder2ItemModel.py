from datetime import datetime
from Backend.Connections.QBcDBConnector import db


class OrderDetailsHeader(db.Model):
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


class OrderItemDetails(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    item_no = db.Column(db.Integer)
    order_id = db.Column(db.String(50))
    item_name = db.Column(db.String(50))
    item_price = db.Column(db.Float)
    item_quantity = db.Column(db.Integer)


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


def CreateOrderItem(
    order_id,
    item_no,
    item_name,
    item_price,
    item_quantity
):
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


def UpdateOrderStatus(order_id, order_status):
    order = OrderDetailsHeader.query.filter_by(order_id=order_id).first()
    order.order_status = order_status
    db.session.commit()
    return order.order_status


def UpdateOrderStatusTimeStamps(order_id, order_status):
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
    elif order_status == 'Order Preparing':
        order.order_prep_time = datetime.now()
    elif order_status == 'Order Accepted':
        order.order_accept_time = datetime.now()
    db.session.commit()
    return order


def CheckOrder(order_id):
    order = OrderDetailsHeader.query.filter_by(order_id=order_id).first()
    if not order:
        return True
    return False

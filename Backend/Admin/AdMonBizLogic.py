from sqlalchemy import func, case, extract
from Backend.Connections.QBcDBConnector import db
from Backend.Models.QBmUserModel import QBUser
from Backend.Models.QBmAdminModel import QBBiz
from Backend.Models.QBmOrder2ItemModel import OrderDetailsHeader, OrderItemDetails
from Backend.Models.QBmLoadMenu import MenuDetails


def GetAdminHomeData():
    total_users = QBUser.query.count()
    total_orders = OrderDetailsHeader.query.count()
    total_items = OrderItemDetails.query.count()
    total_admins = QBBiz.query.count()

    page_data = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_items': total_items,
        'total_admins': total_admins
    }

    return page_data

def custom_mapping(row):
    return {field: getattr(row, field) for field in row._fields}


def GetAdminDashboardData():
    dashboard_data = {
        "orderTrends": [],
        "popularDishes": [],
        "customerSatisfaction": {},
        "orderStatus": {},
        "deliveryStats": {},
        "userGrowth": []
    }

    # Fetch order trends data
    order_trends = (
        db.session.query(
            func.strftime('%Y-%m', OrderDetailsHeader.order_rcv_time).label('month'),
            func.count(OrderDetailsHeader.order_id).label('orders')
        )
        .group_by(func.strftime('%Y-%m', OrderDetailsHeader.order_rcv_time))
        .order_by(func.strftime('%Y-%m', OrderDetailsHeader.order_rcv_time))
        .all()
    )

    for trend in order_trends:
        dashboard_data['orderTrends'].append(custom_mapping(trend))

    # Fetch popular dishes data
    popular_dishes = (
        db.session.query(
            OrderItemDetails.item_name.label('dish'),
            func.count(OrderItemDetails.item_name).label('orders'),
            func.sum(OrderItemDetails.item_quantity).label('qty')
        )
        .group_by(OrderItemDetails.item_name)
        .order_by(func.count(OrderItemDetails.item_name).desc())
        .order_by(func.sum(OrderItemDetails.item_quantity).desc())
        .all()
    )

    for dish in popular_dishes:
        dashboard_data['popularDishes'].append(custom_mapping(dish))

    # Fetch customer satisfaction data
    customer_satisfaction = (
        db.session.query(
            func.sum(case((MenuDetails.item_reviews >= 4, 1), else_=0)).label('excellent'),
            func.sum(case((MenuDetails.item_reviews >= 3, 1), else_=0)).label('good'),
            func.sum(case((MenuDetails.item_reviews >= 2, 1), else_=0)).label('fair'),
            func.sum(case((MenuDetails.item_reviews < 2, 1), else_=0)).label('poor')
        )
        .first()
    )

    dashboard_data['customerSatisfaction'] = custom_mapping(customer_satisfaction)

    # Fetch Order Status data
    order_status = (
        db.session.query(
            func.sum(case((
                OrderDetailsHeader.order_status == 'Order Placed', 1), else_=0
            )).label('placed'),
            func.sum(case((
                OrderDetailsHeader.order_status == 'Order Confirmed', 1), else_=0
            )).label('confirmed'),
            func.sum(case((
                OrderDetailsHeader.order_status == 'Order Ready', 1), else_=0
            )).label('ready'),
            func.sum(case((
                OrderDetailsHeader.order_status == 'Captain Assigned', 1), else_=0
            )).label('captain'),
            func.sum(case((
                OrderDetailsHeader.order_status == 'Out for Delivery', 1), else_=0
            )).label('out_for_delivery'),
            func.sum(case((
                OrderDetailsHeader.order_status == 'Delivered', 1), else_=0
            )).label('delivered'),
            func.sum(case((
                OrderDetailsHeader.order_status == 'Order Cancelled', 1), else_=0
            )).label('cancelled')
        )
        .first()
    )

    dashboard_data['orderStatus'] = custom_mapping(order_status)

    # Fetch Delivery Stats data
    delivery_stats = (
        db.session.query(
            func.sum(case((
                func.abs(extract(
                    'minute', OrderDetailsHeader.order_delivered_time - OrderDetailsHeader.order_rcv_time
                )) <= 10, 1
            ), else_=0)).label('on_time'),
            func.sum(case((
                func.abs(extract(
                    'minute', OrderDetailsHeader.order_delivered_time - OrderDetailsHeader.order_rcv_time
                )) >= 10, 1
            ), else_=0)).label('late'),
            func.sum(case((OrderDetailsHeader.order_status == 'Order Cancelled', 1), else_=0)).label('cancelled')
        )
        .first()
    )

    dashboard_data['deliveryStats'] = custom_mapping(delivery_stats)

    # Fetch User Growth data
    user_growth = (
        db.session.query(
            func.strftime('%Y-%m', QBUser.created_at).label('month'),
            func.count(QBUser.username).label('users')
        )
        .group_by(func.strftime('%Y-%m', QBUser.created_at))
        .order_by(func.strftime('%Y-%m', QBUser.created_at))
        .all()
    )

    for growth in user_growth:
        dashboard_data['userGrowth'].append(custom_mapping(growth))

    return dashboard_data

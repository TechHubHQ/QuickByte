# ================================================================================================
# QuickByte Food Delivery Application

# This is the main application module for the QuickByte food delivery service.
# It handles various routes and functionalities such as user authentication,
# restaurant listing, menu display, order placement, payment, order tracking,
# and user profile management.

# The application is built using the Flask web framework and SQLAlchemy for database
# operations. It integrates with other modules and components to provide a
# comprehensive food delivery experience.
# ================================================================================================

import os
import logging
from waitress import serve
from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask import request, session
from sqlalchemy import func
from datetime import datetime
from dotenv import load_dotenv
from Backend.Admin import admin_bp
from Backend.Connections.QBcDBConnector import init_db
from Backend.Models.QBmLoadRestaurantsByID import RestaurantsByLoc
from Backend.Models.QBmAddressModel import Address, CreateAddress
from Backend.Models.QBmLoadMenu import MenuDetails
from Backend.Models.QBmUserModel import QBUser, ValidateUser, CreateUser, CheckUser
from Backend.Models.QBmOrder2ItemModel import OrderDetailsHeader, OrderItemDetails, UpdateOrderStatusTimeStamps
from Backend.Controllers.QBcrFormCreator import LoginForm, SignupForm, AddressDetailsForm
from Backend.Controllers.QBcrUserController import UserController
from Backend.Logic.QBlPaymentHandler import HandlePayment
from Backend.Logic.QBlOrderHandler import HandleOrderGeneration, generate_order_id
from Config.AppConfig import Config
from Config.PyLogger import RollingFileHandler
import sys

app = Flask(__name__, template_folder='./Frontend/Templates', static_folder='./Frontend/Static')
app.config.from_object(Config)
app.register_blueprint(admin_bp)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, app.config['UPLOAD_FOLDER_RELATIVE'])
app.config['QR_CODE_FOLDER'] = os.path.join(base_dir, app.config['QR_FOLDER_RELATIVE'])
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, 'config', '.env')
load_dotenv(env_path)
APP_LOG_DIR = os.environ.get("APP_LOG_DIR")
init_db(app)


# Page Routes
@app.route('/')
def home():
    app.logger.info(f"{session.get('username')} -- Rendering home page.")
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- User already in session. Redirecting to landing page.")
        return redirect(url_for('landing'))
    else:
        app.logger.info("User accessed home page.")
        return render_template('Home.html')


@app.route('/landing')
def landing():
    try:
        if 'username' in session:
            app.logger.info(f"{session.get('username')} -- Accessing landing page.")
            return render_template('Landing.html')
        else:
            app.logger.warning("User not logged in. Redirecting to login page.")
            return redirect(url_for('login'))
    except Exception as e:
        app.logger.error(f"Exception while accessing landing page for user {session.get('username')}:\n{e}")
        app.logger.info("Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/restaurants')
def restaurants():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing restaurants page.")
        return render_template('Restaurants.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/menu')
def menu():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing menu page.")
        return render_template('Menu.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/cart')
def cart():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing cart page.")
        return render_template('Cart.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/payment')
def payment():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing payment page.")
        return render_template('Payment.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/pay_via_upi', methods=['POST'])
def pay_via_upi():
    app.logger.info(">> Initiating UPI payment via PaymentHandler. <<")
    username = session.get('username')
    data = request.json
    upi_id = data.get('upi_id')
    paid_amount = data.get('paid_amount')
    payment_type = data.get('payment_type')
    app.logger.info(f"PAYLOAD: {data}")
    app.logger.info(f"Username: {username}, UPI ID: {upi_id}, Paid amount: {paid_amount}, Payment type: {payment_type}")
    result = HandlePayment(payment_type=payment_type, last_paid_amount=paid_amount, username=username, upi_id=upi_id)
    if result:
        app.logger.info("UPI payment successful.")
        return jsonify({'message': 'Payment successful'})
    else:
        app.logger.error("UPI payment failed.")
        return jsonify({'message': 'Payment failed'})


@app.route('/pay_via_card', methods=['POST'])
def pay_via_card():
    app.logger.info("Initiating card payment via PaymentHandler.")
    username = session.get('username')
    data = request.json
    card_number = data.get('card_number')
    cardholder_name = data.get('cardholder_name')
    expiry_date = data.get('expiration_date')
    cvv = data.get('cvv')
    payment_type = data.get('payment_type')
    paid_amount = data.get('paid_amount')
    app.logger.info(f"PAYLOAD: {data}")
    app.logger.info(
        f"Username: {username}, Card Number: {card_number}, Cardholder Name: {cardholder_name}, "
        f"Expiry Date: {expiry_date}, CVV: {cvv}, Payment type: {payment_type}")

    result = HandlePayment(
        username=username,
        payment_type=payment_type,
        card_number=card_number,
        cardholder_name=cardholder_name,
        expiry_date=expiry_date,
        cvv=cvv,
        last_paid_amount=paid_amount
    )

    if result:
        app.logger.info("Card payment successful.")
        return jsonify({'message': 'Payment successful'})
    else:
        app.logger.error("Card payment failed.")
        return jsonify({'message': 'Payment failed'})


@app.route('/order_tracker')
def order_tracker():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing order tracker page.")
        return render_template('OrderTracker.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/place_order', methods=['POST'])
def place_order():
    if 'username' in session:
        username = session['username']
        email = QBUser.query.filter_by(username=username).first().email
        data = request.json
        app.logger.info(f"Received order data: {data}")
        order_id = generate_order_id()
        session['order_id'] = order_id
        restaurant_name = data.get('restaurantName')
        order_amount = float(data.get('orderAmount'))
        order_tax = float(data.get('orderTax'))
        subtotal = float(data.get('subtotal'))
        items = data.get('items')
        order_status = 'Order Placed'
        order_rcv_time = datetime.now()
        order_accept_time = None
        order_prep_time = None
        order_ready_time = None
        captain_assigned_time = None
        out_for_delivery_time = None
        order_delivered_time = None
        order_cancel_time = None
        delivery_to = username
        delv_addr = Address.query.filter_by(email=email).first()
        delivery_addr = (f"{delv_addr.line1}, {delv_addr.landmark}, {delv_addr.district}, "
                         f"{delv_addr.state}, {delv_addr.zip_code}")

        app.logger.info(f"{session.get('username')} -- Placing order.")
        app.logger.info(f"PAYLOAD: {data}")
        app.logger.info(
            f"Username: {username}, Order ID: {order_id}, Restaurant Name: {restaurant_name}, "
            f"Order Amount: {order_amount}, Order Tax: {order_tax}, Subtotal: {subtotal}")

        # Lists to store item details
        item_names = []
        item_prices = []
        item_quantities = []

        # Process each item in the order
        for item in items:
            app.logger.info(f"Processing item: {item}")
            item_name = item.get('name')
            item_price = float(item.get('price').split('₹')[1])  # Extract price without 'Price: ₹' prefix
            item_quantity = int(item.get('quantity'))
            app.logger.info(f"Item details - Name: {item_name}, Price: {item_price}, Quantity: {item_quantity}")
            item_names.append(item_name)
            item_prices.append(item_price)
            item_quantities.append(item_quantity)

        # Create order header
        order_header = HandleOrderGeneration.OrderHeaderCreation(
            username=username,
            order_id=order_id,
            restaurant_name=restaurant_name,
            order_status=order_status,
            order_type='Home Delivery',
            order_base_price=subtotal,
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

        # Create order items
        for i in range(len(item_names)):
            order_item = HandleOrderGeneration.OrderItemCreation(
                order_id=order_id,
                item_no=(i + 1) * 10,
                item_name=item_names[i],
                item_price=item_prices[i],
                item_quantity=item_quantities[i]
            )
            app.logger.info(f"Created order item: {order_item}")

        app.logger.info(f"Order header created: {order_header}")
        return jsonify({'message': 'Order placed successfully'})
    else:
        app.logger.warning("User not logged in.")
        return jsonify({'error': 'User not logged in'})


@app.route('/get_order_details')
def get_order_details():
    if 'username' in session:
        username = session['username']
        order_id = session['order_id']
        order = OrderDetailsHeader.query.filter_by(user_name=username, order_id=order_id).first()
        if order:
            app.logger.info("Fetching order details.")
            order_details = {
                'order_id': order.order_id,
                'delivery_address': order.delivery_addr,
                'order_status': order.order_status,
                'completed_steps': []
            }
            # Define the steps based on order status
            steps = ['Order Placed', 'Order Confirmed', 'Preparing Order',
                     'Order Ready', 'Captain Assigned', 'Out for Delivery', 'Delivered']
            # Add completed steps based on order status
            if order.order_status == 'Order Cancelled':
                app.logger.info("Order has been cancelled.")
                order_details['completed_steps'].append('Order Cancelled')
                return jsonify(order_details)
            else:
                found_current_status = False
                for step in steps:
                    if step == order.order_status:
                        found_current_status = True
                        order_details['completed_steps'].append(step)
                    elif found_current_status:
                        break
                    else:
                        order_details['completed_steps'].append(step)

                app.logger.info(f"{order_id} -- Order details fetched successfully.")
                return jsonify(order_details)
        else:
            app.logger.error(f"{session.get('username')} -- No order found for this user.")
            return jsonify({'error': 'No order found for this user'})
    else:
        app.logger.warning("User not logged in.")
        return jsonify({'error': 'User not logged in'})


@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    if 'username' in session:
        username = session['username']
        order_id = session['order_id']
        order = OrderDetailsHeader.query.filter_by(user_name=username, order_id=order_id).first()
        if order:
            session.pop('order_id', None)  # Remove the order ID from the session
            order.order_status = 'Order Cancelled'
            order.order_cancel_time = datetime.now()
            UpdateOrderStatusTimeStamps(order_id, order.order_status)
            app.logger.info(f"Order {order_id} cancelled successfully. by {session.get('username')}")
            return jsonify({'message': 'Order cancelled successfully'})
        else:
            app.logger.error(f"{session.get('username')} -- No order found for this user.")
    else:
        app.logger.warning("User not logged in.")
    return jsonify({'error': 'Unauthorized access or no order found'})


@app.route('/order_status_tracker')
def order_status_tracker():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing order status tracker page.")
        return render_template('OrderStatusTracker.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/order_status_data', methods=['GET', 'POST'])
def order_status_data():
    if 'username' in session:
        username = session['username']
        data = request.json
        order_id = data.get('order_id')
        orders = OrderDetailsHeader.query.filter_by(user_name=username, order_id=order_id).all()
        for order in orders:
            order_details = {
                'order_id': order.order_id,
                'delivery_address': order.delivery_addr,
                'order_status': order.order_status,
                'completed_steps': []
            }
            # Define the steps based on order status
            steps = ['Order Placed', 'Order Confirmed', 'Preparing Order',
                     'Order Ready', 'Captain Assigned', 'Out for Delivery', 'Delivered']
            # Add completed steps based on order status
            if order.order_status == 'Order Cancelled':
                order_details['completed_steps'].append('Order Cancelled')
                app.logger.info(f"Order {order_id} has been cancelled.")
                return jsonify(order_details)
            else:
                found_current_status = False
                for step in steps:
                    if step == order.order_status:
                        found_current_status = True
                        order_details['completed_steps'].append(step)
                    elif found_current_status:
                        break
                    else:
                        order_details['completed_steps'].append(step)

                app.logger.info(f"Order details fetched for order {order_id} -- {order_details}")
                return jsonify(order_details)
        else:
            app.logger.error(f"{session.get('username')} -- No order found for this user.")
            return jsonify({'error': 'No order found for this user'})
    else:
        app.logger.warning("User not logged in.")
        return jsonify({'error': 'User not logged in'})


@app.route('/my_orders')
def my_orders():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing my orders page.")
        return render_template('MyOrders.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/my_orders_data', methods=['GET', 'POST'])
def my_orders_data():
    if 'username' in session:
        username = session['username']
        app.logger.info(f"Fetching orders data for user {username}.")
        orders = OrderDetailsHeader.query.filter_by(user_name=username).all()
        data = []
        for order in orders:
            order_details = {
                'order_id': order.order_id,
                'restaurant_name': order.restaurant_name,
                'order_status': order.order_status,
                'order_type': order.order_type,
                'order_base_price': order.order_base_price,
                'order_tax': order.order_tax,
                'order_amount': order.order_amount,
                'order_rcv_time': order.order_rcv_time.strftime('%Y-%m-%d %H:%M:%S'),
                'order_accept_time': order.order_accept_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.order_accept_time else None,
                'order_prep_time': order.order_prep_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.order_prep_time else None,
                'order_ready_time': order.order_ready_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.order_ready_time else None,
                'captain_assigned_time': order.captain_assigned_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.captain_assigned_time else None,
                'out_for_delivery_time': order.out_for_delivery_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.out_for_delivery_time else None,
                'order_delivered_time': order.order_delivered_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.order_delivered_time else None,
                'order_cancel_time': order.order_cancel_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if order.order_cancel_time else None,
                'delivery_to': order.delivery_to,
                'delivery_addr': order.delivery_addr,
                'items': []
            }
            items = OrderItemDetails.query.filter_by(order_id=order.order_id).all()
            for item in items:
                item_details = {
                    'item_no': item.item_no,
                    'item_name': item.item_name,
                    'item_price': item.item_price,
                    'item_quantity': item.item_quantity
                }
                order_details['items'].append(item_details)
            data.append(order_details)
        app.logger.info(f"Orders data fetched successfully. -- {data}")
        return jsonify(data)
    else:
        app.logger.warning("User not logged in. Unauthorized access attempted.")
        return jsonify({'error': 'User not logged in or unauthorized access attempted'})


@app.route('/profile')
def profile():
    if 'username' in session:
        user_name = session['username']
        app.logger.info(f"Accessing profile page for user {user_name}.")
        user = QBUser.query.filter_by(username=user_name).first()
        formatted_username = user.username.replace(' ', '_') if user else None
        profile_image_url = GetProfileImage(formatted_username) if formatted_username else None
        app.logger.info(f"Profile image URL: {profile_image_url}")
        return render_template('Profile.html', user=user, profile_image_url=profile_image_url)
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


def GetProfileImage(username):
    username_with_extension = f"{username}.jpg"
    image_path = os.path.join(base_dir, app.config['UPLOAD_FOLDER_RELATIVE'], username_with_extension)
    return image_path if os.path.exists(image_path) else None


@app.route('/my_address')
def my_address():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing my address page.")
        return render_template('MyAddress.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/my_address_data')
def my_address_data():
    if 'username' in session:
        username = session['username']
        app.logger.info(f"Fetching address data for user {username}.")
        email = QBUser.query.filter_by(username=username).first().email
        addresses = Address.query.filter_by(email=email).all()
        data = []
        for address in addresses:
            address_details = {
                'address_line1': address.line1,
                'address_landmark': address.landmark,
                'district': address.district,
                'state': address.state,
                'pincode': address.zip_code,
            }
            data.append(address_details)
        app.logger.info(f"Address data fetched successfully. -- {data}")
        return jsonify(data)
    else:
        app.logger.warning("User not logged in.")
        return jsonify({'error': 'User not logged in'})


@app.route("/help")
def help():
    app.logger.info(f"{session.get('username')} -- Accessing help page.")
    app.logger.debug(f"Session: {session}")
    if 'username' in session:
        return render_template('Help_Center.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


# QBUser Module
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session['username'] = username
        result = CheckUser(username, password)
        if result == "Admin Login":
            return redirect(url_for('admin.login'))
        elif result:
            app.logger.info(f"User {username} logged in successfully.")
            return redirect(url_for('landing'))
        else:
            flash('Invalid username or password', 'danger')
            app.logger.warning(f"Failed login attempt for username: {username}")
            return redirect(url_for('login'))
    return render_template('Login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # Get form data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        session['email'] = email

        # Validate user input
        validation_result = ValidateUser(username, email, password, confirm_password)

        if validation_result is None:
            # Create a new user
            CreateUser(username, email, password)
            # TODO: Implement Mailing Service After creating Domain (Deployment)
            # SendWelcomeEmail(email, username)
            app.logger.info(f"New user {username} signed up successfully.")
            flash('Account created successfully!', 'success')
            return redirect(url_for('address'))
        else:
            flash(validation_result, 'danger')

    return render_template('SignUp.html', form=form)


# Address Module
@app.route('/address', methods=['GET', 'POST'])
def address():
    email = session['email']
    form = AddressDetailsForm()
    app.logger.info(f"Accessing address page for user with email: {email}.")
    app.logger.debug(
        f"Received a {request.method} request with form validation result: {form.validate_on_submit()}, "
        f"errors: {form.errors}, and form data: {request.form}")
    if request.method == 'POST' and form.validate_on_submit():
        user_email = email
        line1 = request.form['line1']
        land_mark = request.form['landmark']
        state = request.form['state']
        district = request.form['district']
        zip_code = request.form['zip_code']
        CreateAddress(user_email, line1, land_mark, district, state, zip_code)
        app.logger.info("Address saved successfully.")
        flash('Address saved successfully!', 'success')
        app.logger.info("Redirecting to login page.")
        return redirect(url_for('login'))

    return render_template('AddressDetails.html', form=form)


@app.route('/settings')
def settings():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Accessing settings page.")
        return render_template('Settings.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    # Remove the username from the session
    username = session.pop('username', None)
    app.logger.info(f"User {username} logged out.")
    return redirect(url_for('home'))


@app.route("/associate")
def associate():
    if 'username' in session:
        app.logger.info(f"{session.get('username')} -- Registering to become Associate")
        return render_template("Associate.html")
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


# Admin Module
@app.route('/admin')
def admin():
    app.logger.info("Accessing admin page.")
    app.logger.debug(f"Session: {session}")
    if 'username' in session:
        return render_template('Admin.html')
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


# API Module
@app.route('/api/images')
def GetImages():
    morning_images = [
        'Idly.png', 'dosa.png', 'bonda.png', 'poori.png', 'sandwich.png', 'vada.png', 'cornflakes.png',
        'chapati.png', 'poha.png', 'salad.png', 'cereals.png', 'fruits.png', 'pancake.png', 'juice.png',
        'upma.png', 'utappam.png', 'coffee.png', 'tea.png'
    ]
    afternoon_images = [
        'veg_biryani.png', 'south-indian.png', 'north-indian.png', 'chinese.png', 'shawarma.png',
        'salad.png', 'burger.png', 'margarita_pizza.png', 'cake.png', 'paratha.png', 'rolls.png', 'pasta.png',
        'dosa.png', 'ice-cream.png', 'baath.png', 'khichidi.png', 'noodles.png', 'shakes.png'
    ]
    evening_images = [
        'samosa.png', 'chicken-manchuria.png', 'fries.png', 'noodles.png', 'beverages.png',
        'ice-cream.png', 'fish.png', 'crispy-potato.png', 'pakoda.png', 'punugulu.png', 'maggi.png',
        'sandwich.png', 'bread-omlette.png', 'momos.png', 'tacos.png', 'rolls.png', 'toast.png',
        'bread-halwa.png'
    ]
    night_images = [
        'veg_biryani.png', 'chicken-manchuria.png', 'butternut-squash.png', 'panner-pasanda.png', 'tofu-curry.png',
        'baked-feta.png', 'chicken-pot.png', 'spaghetti_carbonara.png', 'khichidi.png', 'dal_makhani.png',
        'baath.png', 'chicken-florentine.png', 'burger.png', 'margarita_pizza.png', 'cake.png', 'noodles.png',
        'shakes.png', 'beverages.png'
    ]

    current_hour = datetime.now().hour

    if 6 <= current_hour < 10:
        images = morning_images
    elif 10 <= current_hour < 16:
        images = afternoon_images
    elif 16 <= current_hour < 19:
        images = evening_images
    else:
        images = night_images

    app.logger.info(f"{datetime.now()} -- images rendered for {current_hour} hour slot")
    return jsonify(images)


@app.route('/api/restaurants')
def GetRestaurants():
    if 'username' in session:
        username = session['username']
        app.logger.info(f"Accessing restaurant API for user {username}.")
        user = QBUser.query.filter_by(username=username).first()
        email = user.email
        district = Address.query.filter_by(email=email).first().district
        restaurants = RestaurantsByLoc.query.filter(func.lower(RestaurantsByLoc.address).
                                                    like(func.lower(f'%{district}%'))).all()

        # Create a list to store the restaurant information
        restaurant_info = []

        # Loop through the restaurants and create a dictionary containing all the required information
        for restaurant in restaurants:
            restaurant_dict = {
                'restaurant_name': restaurant.restaurant_name,
                'number_of_reviews': restaurant.num_reviews,
                'rating': restaurant.rating,
                'ranking': restaurant.ranking,
                'web_url': restaurant.web_url,
                'image_url': restaurant.image_url
            }
            restaurant_info.append(restaurant_dict)

        # Return the list of restaurant information as JSON
        app.logger.info(f"Returning {len(restaurant_info)} for {district} for user {username}.\n "
                        f"rendered restaurants: {restaurant_info}"
                        )
        return jsonify(restaurant_info)
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/api/menu')
def GetMenu():
    if 'username' in session:
        app.logger.info("Accessing menu API.")
        menu_items = MenuDetails.query.all()
        # Create a list to store the menu information
        menu_info = []
        # Loop through the menu items and create a dictionary containing all the required information
        for menu in menu_items:
            menu_dict = {
                'cuisine': menu.cuisine_name,
                'item_category': menu.item_category,
                'item_name': menu.item_name,
                'item_type': menu.item_type,
                'item_price': menu.item_price,
                'item_description': menu.item_description,
                'item_rating': menu.item_reviews
            }
            menu_info.append(menu_dict)
        app.logger.info(f"Returning {len(menu_info)} menu items.\n rendered menu item: {menu_info}")
        return jsonify(menu_info)
    else:
        app.logger.warning("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'username' in session:
        profile_img = request.files['profile_image']

        if profile_img:
            UserController.SaveImage(session['username'], profile_img)
            app.logger.info("Image uploaded successfully.")
            return jsonify({'message': 'Image uploaded successfully'})
        else:
            app.logger.warning("No image selected.")
            return jsonify({'message': 'No image selected'})
    else:
        app.logger.warning("User not logged in.")
        return jsonify({'message': 'User not logged in'})


@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = request.form.get('username')
    password = request.form.get('password')
    if username:
        old_pass = QBUser.query.filter_by(username=username).first().password
        if old_pass == password:
            flash('New password cannot be same as old password', 'danger')
            return redirect(url_for('settings'))
        else:
            UserController.UpdateUser(username, password)
            flash('User details updated Successfully', 'success')
            app.logger.info(f"User details updated for username: {username}")
            return redirect(url_for('settings'))
    elif 'username' in session:
        username = session['username']

        if CheckUser(username, password):
            flash('New password cannot be same as old password', 'danger')
            return redirect(url_for('settings'))
        else:
            UserController.UpdateUser(username, password)
            flash('User details updated Successfully', 'success')
            app.logger.info(f"User details updated for username: {username}")
            return redirect(url_for('settings'))
    else:
        flash('User not logged in', 'danger')
        app.logger.warning("User not logged in.")
        return redirect(url_for('login'))


@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    if 'username' in session:
        username = session['username']
        preferences = request.form.get('email_notifications')
        preferences = True if preferences == 'on' else False
        UserController.UpdatePreferences(username, preferences)
        app.logger.info(f"Updated preferences for user: {username}")
        return redirect(url_for('settings'))
    else:
        app.logger.warning("User not logged in.")
        return redirect(url_for('login'))


@app.route('/update_delv', methods=['POST'])
def update_delv():
    line1 = request.form.get('line1')
    landmark = request.form.get('landmark')
    state = request.form.get('state')
    district = request.form.get('district')
    preferred_delv_start_time = request.form.get('delv_start_time')
    preferred_delv_end_time = request.form.get('delv_end_time')
    if 'username' in session:
        username = session['username']
        user = QBUser.query.filter_by(username=username).first()
        email = user.email
        UserController.UpdateDelivery(
            email,
            line1,
            landmark,
            state,
            district,
            preferred_delv_start_time,
            preferred_delv_end_time
        )
        app.logger.info(f"Updated delivery details for user: {username} \nPAYLOAD: "
                        f"{line1, landmark, state, district, preferred_delv_start_time, preferred_delv_end_time}"
                        )
    return redirect(url_for('settings'))


if __name__ == '__main__':
    current_date = datetime.now().strftime('%Y-%m-%d')
    if len(sys.argv) >= 3:
        CORE_DEV = os.environ.get("CORE_DEV")

        if sys.argv[1] == "--PROD" and sys.argv[2] in CORE_DEV:
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            file_handler = RollingFileHandler(APP_LOG_DIR, 'QuickByteAPP.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            # Run the Waitress server
            app.logger.info(f"{datetime.now()} --> APP Started")
            serve(app, host='0.0.0.0', port=8080, threads=5)
    elif sys.argv[1] == "--debug":
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = RollingFileHandler(APP_LOG_DIR, 'QuickByteAPP_DEBUG.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        app.run(debug=True)
    else:
        print("Usage: for debug mode python APP.py --debug")
        print("Usage: for production mode python APP.py --PROD <CORE_DEV>")

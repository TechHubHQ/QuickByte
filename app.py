import os
from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask import request, session
from sqlalchemy import func
from datetime import datetime
from Backend.Connections.QBcDBConnector import init_db
from Backend.Models.QBmLoadRestaurantsByID import RestaurantsByLoc
from Backend.Models.QBmAddressModel import Address, CreateAddress
from Backend.Models.QBmLoadMenu import MenuDetails
from Backend.Models.QBmUserModel import QBUser, ValidateUser, CreateUser, CheckUser
from Backend.Models.QBmOrder2ItemModel import OrderDetailsHeader, UpdateOrderStatusTimeStamps
from Backend.Controllers.QBcrFormCreator import LoginForm, SignupForm, AddressDetailsForm
from Backend.Controllers.QBcrUserController import UserController
from Backend.Logic.QBlPaymentHandler import HandlePayment
from Backend.Logic.QBlOrderHandler import HandleOrderGeneration, generate_order_id
from Config.AppConfig import Config

app = Flask(__name__, template_folder='./Frontend/Templates', static_folder='./Frontend/Static')
app.config.from_object(Config)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, app.config['UPLOAD_FOLDER_RELATIVE'])
app.config['QR_CODE_FOLDER'] = os.path.join(base_dir, app.config['QR_FOLDER_RELATIVE'])
init_db(app)


# Page Routes
@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/landing')
def landing():
    print(session)
    try:
        if 'username' in session:
            return render_template('Landing.html')
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print("\n----------------------------------------------------------------------------")
        print(f"Exception while accessing landing page for user {session['username']}: \n{e}")
        print("-----------------------------------------------------------------------------\n")
        return redirect(url_for('login'))


@app.route('/restaurants')
def restaurants():
    if 'username' in session:
        return render_template('Restaurants.html')
    else:
        return redirect(url_for('login'))


@app.route('/menu')
def menu():
    print("\n------------------------------------------------------------------")
    print(session)
    print("------------------------------------------------------------------\n")
    if 'username' in session:
        return render_template('Menu.html')
    else:
        return redirect(url_for('login'))


@app.route('/cart')
def cart():
    print(session)
    if 'username' in session:
        return render_template('Cart.html')

    else:
        return redirect(url_for('login'))


@app.route('/payment')
def payment():
    if 'username' in session:
        return render_template('Payment.html')
    else:
        return redirect(url_for('login'))


@app.route('/pay_via_upi', methods=['POST'])
def pay_via_upi():
    # Extract UPI ID from the request JSON data
    username = session.get('username')
    data = request.json
    upi_id = data.get('upi_id')
    paid_amount = data.get('paid_amount')
    payment_type = data.get('payment_type')
    print(f"UPI ID: {upi_id}, username: {username}, paid amount: {paid_amount}, payment type: {payment_type}")

    result = HandlePayment(payment_type=payment_type, last_paid_amount=paid_amount, username=username, upi_id=upi_id)

    if result:
        return jsonify({'message': 'Payment successful'})
    else:
        return jsonify({'message': 'Payment failed'})


@app.route('/pay_via_card', methods=['POST'])
def pay_via_card():
    # Extract card details from the request
    username = session.get('username')
    data = request.json
    card_number = data.get('card_number')
    cardholder_name = data.get('cardholder_name')
    expiry_date = data.get('expiration_date')
    cvv = data.get('cvv')
    payment_type = data.get('payment_type')
    paid_amount = data.get('paid_amount')

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
        return jsonify({'message': 'Payment successful'})
    else:
        return jsonify({'message': 'Payment failed'})


@app.route('/order_tracker')
def order_tracker():
    if 'username' in session:
        return render_template('OrderTracker.html')
    else:
        return redirect(url_for('login'))


@app.route('/place_order', methods=['POST'])
def place_order():
    if 'username' in session:
        username = session['username']
        email = QBUser.query.filter_by(username=username).first().email
        data = request.json
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
        delivery_addr = f"{delv_addr.line1}, {delv_addr.landmark}, {delv_addr.district}, {delv_addr.state}, {delv_addr.zip_code}"

        # Lists to store item details
        item_names = []
        item_prices = []
        item_quantities = []

        # Process each item in the order
        for item in items:
            print(f"item: {item}")
            item_name = item.get('name')
            item_price = float(item.get('price').split('₹')[1])  # Extract price without 'Price: ₹' prefix
            item_quantity = int(item.get('quantity'))
            print(f"data: {item_name}, {item_price}, {item_quantity}")
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
            print(order_item)
        print(order_header)
    return jsonify({'message': 'Order placed successfully'})


@app.route('/get_order_details')
def get_order_details():
    # Assuming you have a session variable with the username
    if 'username' in session:
        username = session['username']
        order_id = session['order_id']
        order = OrderDetailsHeader.query.filter_by(user_name=username, order_id=order_id).first()
        if order:
            order_details = {
                'order_id': order.order_id,
                'delivery_address': order.delivery_addr,
                'order_status': order.order_status,
                'completed_steps': []  # This will be populated with completed steps based on the status
            }
            # Define the steps based on order status
            steps = ['Order Placed', 'Order Confirmed', 'Preparing Order',
                     'Order Ready', 'Captain Assigned', 'Out for Delivery', 'Delivered']
            # Add completed steps based on order status
            found_current_status = False
            for step in steps:
                if step == order.order_status:
                    found_current_status = True
                    order_details['completed_steps'].append(step)
                elif found_current_status:
                    break
                else:
                    order_details['completed_steps'].append(step)

            return jsonify(order_details)
        else:
            return jsonify({'error': 'No order found for this user'})
    else:
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
            return jsonify({'message': 'Order cancelled successfully'})


@app.route('/my_orders')
def my_orders():
    if 'username' in session:
        return render_template('MyOrders.html')
    else:
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'username' in session:
        user_name = session['username']
        user = QBUser.query.filter_by(username=user_name).first()
        formatted_username = user.username.replace(' ', '_') if user else None
        profile_image_url = GetProfileImage(formatted_username) if formatted_username else None
        print(f"url: {profile_image_url}")
        return render_template('Profile.html', user=user, profile_image_url=profile_image_url)
    else:
        return redirect(url_for('login'))


def GetProfileImage(username):
    username_with_extension = f"{username}.jpg"
    image_path = os.path.join(base_dir, app.config['UPLOAD_FOLDER_RELATIVE'], username_with_extension)
    return image_path if os.path.exists(image_path) else None


@app.route("/help")
def help():
    print("\n------------------------------------------------------------------")
    print(session)
    print("------------------------------------------------------------------\n")
    if 'username' in session:
        return render_template('Help.html')
    else:
        return redirect(url_for('login'))


# QBUser Module
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session['username'] = username

        if CheckUser(username, password):
            return redirect(url_for('landing'))
        else:
            flash('Invalid username or password', 'danger')
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
            flash('Account created successfully!', 'success')
            return redirect(url_for('address'))
        else:
            flash(validation_result, 'danger')

    return render_template('Signup.html', form=form)


# Address Module
@app.route('/address', methods=['GET', 'POST'])
def address():
    email = session['email']
    form = AddressDetailsForm()
    print("\n---------------------------------------------------------------------------------------------------")
    print(f"received a {request.method} request {form.validate_on_submit()} and {form.errors} and {request.form}")
    print("---------------------------------------------------------------------------------------------------\n")
    if request.method == 'POST' and form.validate_on_submit():
        user_email = email
        line1 = request.form['line1']
        land_mark = request.form['landmark']
        state = request.form['state']
        district = request.form['district']
        zip_code = request.form['zip_code']
        CreateAddress(user_email, line1, land_mark, district, state, zip_code)
        flash('Address saved successfully!', 'success')
        print("redirecting to login page..")
        return redirect(url_for('login'))

    return render_template('AddressDetails.html', form=form)


@app.route('/settings')
def settings():
    return render_template('Settings.html')


@app.route("/logout")
def logout():
    # Remove the email from the session
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/associate")
def associate():
    if 'username' in session:
        return render_template("Associate.html")
    else:
        redirect(url_for('login'))


# Admin Module
@app.route('/admin')
def admin():
    print(session)
    if 'username' in session:
        return render_template('Admin.html')
    else:
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

    return jsonify(images)


# noinspection PyShadowingNames
@app.route('/api/restaurants')
def GetRestaurants():
    if 'username' in session:
        username = session['username']
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
        return jsonify(restaurant_info)


# noinspection PyShadowingNames
@app.route('/api/menu')
def GetMenu():
    if 'username' in session:
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
        # Return the list of menu information as JSON
        return jsonify(menu_info)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'username' in session:
        profile_img = request.files['profile_image']

        if profile_img:
            UserController.SaveImage(session['username'], profile_img)
            return jsonify({'message': 'Image uploaded successfully'})
        else:
            print("No image selected")
            return jsonify({'message': 'No image selected'})
    else:
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
            print("\n------------------------------------------------------------------------")
            print(f"user details updated with data --> username: {username}, key: {password}")
            print("------------------------------------------------------------------------\n")
            return redirect(url_for('settings'))
    elif 'username' in session:
        username = session['username']

        if CheckUser(username, password):
            flash('New password cannot be same as old password', 'danger')
            return redirect(url_for('settings'))
        else:
            UserController.UpdateUser(username, password)
            flash('User details updated Successfully', 'success')
            print("\n------------------------------------------------------------------------")
            print(f"user details updated with data --> username: {username}, key: {password}")
            print("------------------------------------------------------------------------\n")
            return redirect(url_for('settings'))
    else:
        flash('User not logged in', 'danger')
        return redirect(url_for('login'))


@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    if 'username' in session:
        username = session['username']
        preferences = request.form.get('email_notifications')
        preferences = True if preferences == 'on' else False
        UserController.UpdatePreferences(username, preferences)
        return redirect(url_for('settings'))
    else:
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
    return redirect(url_for('settings'))


if __name__ == '__main__':
    app.run(debug=True)

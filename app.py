import os
from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask import request, session
from sqlalchemy import func
from datetime import datetime
from Backend.Connections.QBcDBConnector import init_db
from Backend.Models.QBmAddressModel import Address, CreateAddress
from Backend.Models.QBmUserModel import QBUser, ValidateUser, CreateUser, CheckUser
from Backend.Models.QBmLoadRestaurantsByID import RestaurantsByLoc
from Backend.Controllers.QBcrFormCreator import LoginForm, SignupForm, AddressDetailsForm
from Backend.Controllers.QBcrUserController import UserController
from Config.AppConfig import Config

app = Flask(__name__, template_folder='./Frontend/Templates', static_folder='./Frontend/Static')
app.config.from_object(Config)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, app.config['UPLOAD_FOLDER_RELATIVE'])
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


@app.route('/orders')
def orders():
    print(session)
    if 'username' in session:
        return render_template('Orders.html')
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
        'biryani.png', 'south-indian.png', 'north-indian.png', 'chinese.png', 'shawarma.png',
        'salad.png', 'burger.png', 'pizza.png', 'cake.png', 'paratha.png', 'rolls.png', 'pasta.png',
        'dosa.png', 'ice-cream.png', 'baath.png', 'khichidi.png', 'noodles.png', 'shakes.png'
    ]
    evening_images = [
        'samosa.png', 'chicken-manchuria.png', 'fries.png', 'noodles.png', 'beverages.png',
        'ice-cream.png', 'fish.png', 'crispy-potato.png', 'pakoda.png', 'punugulu.png', 'maggi.png',
        'sandwich.png', 'bread-omlette.png', 'momos.png', 'tacos.png', 'rolls.png', 'toast.png',
        'bread-halwa.png'
    ]
    night_images = [
        'biryani.png', 'chicken-manchuria.png', 'butternut-squash.png', 'panner-pasanda.png', 'tofu-curry.png',
        'baked-feta.png', 'chicken-pot.png', 'sphagetti-carbonara.png', 'khichidi.png', 'dal-makkhani.png',
        'baath.png', 'chicken-florentine.png', 'burger.png', 'pizza.png', 'cake.png', 'noodles.png',
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


def GetProfileImage(username):
    username_with_extension = f"{username}.jpg"
    image_path = os.path.join(base_dir, app.config['UPLOAD_FOLDER_RELATIVE'], username_with_extension)
    return image_path if os.path.exists(image_path) else None


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

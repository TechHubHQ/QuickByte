from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask import request, session
from datetime import datetime
from Backend.Controllers.QBcrFormCreator import LoginForm, SignupForm, AddressDetailsForm
from Backend.Models.QBmLoadUsers import ValidateUser, CreateUser, CheckUser
from Backend.Models.QBmLoadAddress import CreateAddress
from Backend.Connections.QBcDBConnector import init_db
from Config.AppConfig import Config

app = Flask(__name__, template_folder='./Frontend/Templates', static_folder='./Frontend/Static')
app.config.from_object(Config)
init_db(app)


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
        print(e)
        return redirect(url_for('login'))


@app.route('/menu')
def menu():
    print(session)
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
    print(session)
    if 'username' in session:
        return render_template('Profile.html')
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
    print(f"received a {request.method} request {form.validate_on_submit()} and {form.errors} and {request.form}")
    if request.method == 'POST' and form.validate_on_submit():
        user_email = email
        line1 = request.form['line1']
        land_mark = request.form['landmark']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        CreateAddress(user_email, line1, land_mark, city, state, zip_code)
        flash('Address saved successfully!', 'success')
        print("redirecting to landing page..")
        return redirect(url_for('landing'))

    return render_template('AddressDetails.html', form=form)


@app.route('/favorites')
def favorites():
    return render_template('Favorites.html')


@app.route('/settings')
def settings():
    return render_template('Settings.html')


@app.route("/logout")
def logout():
    # Remove the email from the session
    session.pop('username', None)
    return redirect(url_for('home'))


# Admin Module
@app.route('/admin')
def admin():
    print(session)
    if 'username' in session:
        return render_template('Admin.html')
    else:
        return redirect(url_for('login'))


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


if __name__ == '__main__':
    app.run(debug=True)

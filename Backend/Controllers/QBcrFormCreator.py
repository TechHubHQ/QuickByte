# =================================================================================================================================
# This module defines various Flask-WTF (Web Forms) forms used for user authentication, address management,
# and restaurant/dish management in the application.

# It includes the following forms:

# 1. User Module:
#    - LoginForm: For user login with fields for username and password.
#    - SignupForm: For user registration with fields for username, email, password, and confirm password.
#    - AddressDetailsForm: For capturing user's address details with fields for line1, landmark, state, district, and zip code.

# 2. Admin Module:
#    - RestaurantForm: For adding/editing restaurant details with fields for name, address, city, state, zip code, and photo.
#    - DishForm: For adding/editing dish details with fields for name, description, price, and photo.

# These forms ensure data validation and can be used in views and templates for rendering and processing form data.
# ================================================================================================================================

# ========================================================
# Imports/Packages
# ========================================================

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# User Module
class LoginForm(FlaskForm):
    """
    Form for user login with fields for username and password.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    """
    Form for user registration with fields for username, email, password, and confirm password.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class AddressDetailsForm(FlaskForm):
    """
    Form for capturing user's address details with fields for line1, landmark, state, district, and zip code.
    """
    line1 = StringField('Address Line 1', validators=[DataRequired()])
    land_mark = StringField('Land Mark')
    state = StringField('State', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Save Address')


# Admin Module
class RestaurantForm(FlaskForm):
    """
    Form for adding/editing restaurant details with fields for name, address, city, state, zip code, and photo.
    """
    name = StringField('Restaurant Name', validators=[DataRequired()])
    line1 = StringField('Address Line 1', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    photo = FileField('Photo')
    submit = SubmitField('Save Restaurant')


class DishForm(FlaskForm):
    """
    Form for adding/editing dish details with fields for name, description, price, and photo.
    """
    name = StringField('Dish Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    photo = FileField('Photo')
    submit = SubmitField('Save Dish')

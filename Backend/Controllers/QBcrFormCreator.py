# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# User Module
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class AddressDetailsForm(FlaskForm):
    line1 = StringField('Address Line 1', validators=[DataRequired()])
    land_mark = StringField('Land Mark')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Save Address')


# Admin Module
class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired()])
    line1 = StringField('Address Line 1', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    photo = FileField('Photo')
    submit = SubmitField('Save Restaurant')


class DishForm(FlaskForm):
    name = StringField('Dish Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    photo = FileField('Photo')
    submit = SubmitField('Save Dish')

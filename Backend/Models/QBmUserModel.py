# ====================================================================================================
# Module for defining the QBUser class and related functions.

# This module contains the definition of the QBUser class, which represents user information
# in the database. It also includes functions for user validation, authentication, and creation.

# The QBUser class maps to the 'qb_user' table in the database.

# ====================================================================================================

# ====================================================================
# Imports/Packages
# ====================================================================
from Backend.Connections.QBcDBConnector import db, bcrypt


# ============================================================
# QBUser Table DataBase Schema
# ============================================================
class QBUser(db.Model):
    """
    Model class for representing user information in the database.

    Attributes:
        id (int): The primary key ID of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
    """
    
    __tablename__ = 'qb_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


def ValidateUser(username, email, password, confirm_password):
    """
    Validates user information during registration.

    Args:
        username (str): The username provided during registration.
        email (str): The email address provided during registration.
        password (str): The password provided during registration.
        confirm_password (str): The confirmed password provided during registration.

    Returns:
        str or None: An error message if validation fails, or None if validation is successful.
    """
    
    existing_username = QBUser.query.filter_by(username=username).first()
    if existing_username:
        return "Username is already taken. Please choose another."

    # Check for email uniqueness
    existing_email = QBUser.query.filter_by(email=email).first()
    if existing_email:
        return "Email is already registered. Please use another email."

    # Check password length
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # Check password complexity (you can add more checks based on your requirements)
    if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
        return "Password must contain both letters and numbers."

    # Check if passwords match (for sign-up)
    if confirm_password is not None and password != confirm_password:
        return "Passwords do not match."

    # If all checks pass, return None (indicating successful validation)
    return None


def CheckUser(username, password):
    """
    Validates user credentials during login.

    Args:
        username (str): The username provided during login.
        password (str): The password provided during login.

    Returns:
        QBUser or None: The user object if authentication is successful, else None.
    """
    
    user = QBUser.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None


def CreateUser(username, email, password):
    """
    Creates a new user entry in the database.

    Args:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The password of the new user.

    Returns:
        None
    """
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = QBUser(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

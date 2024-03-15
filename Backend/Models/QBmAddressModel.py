# ==========================================================================================================================
# This module defines the Address model and provides a function to create new address records in the database.

# The Address model represents a user's delivery address information and includes the following fields:
# - id: The primary key for the address record.
# - email: The email address of the user associated with this address (foreign key referencing the QBUser model).
# - line1: The first line of the address.
# - landmark: The landmark or additional address details.
# - district: The district of the address.
# - state: The state of the address.
# - zip_code: The zip code of the address.
# - preferred_delv_start_time: The preferred start time for delivery (default: 00:00).
# - preferred_delv_end_time: The preferred end time for delivery (default: 00:00).

# The CreateAddress function is provided to create a new address record in the database with the given user email
# and address details.

# This module should be imported and used in conjunction with the SQLAlchemy database connection and the QBUser model
# to manage address information in the application.
# ========================================================================================================================


# =========================================================================
# Imports/Packages
# =========================================================================
from Backend.Connections.QBcDBConnector import db


# =========================================================================
# Address Table DataBase Schema
# =========================================================================
class Address(db.Model):
    """
    This class represents the Address model for storing user delivery address information.

    Attributes:
        id (int): The primary key for the address record.
        email (str): The email address of the user associated with this address (foreign key referencing the QBUser model).
        line1 (str): The first line of the address.
        landmark (str): The landmark or additional address details.
        district (str): The district of the address.
        state (str): The state of the address.
        zip_code (str): The zip code of the address.
        preferred_delv_start_time (str): The preferred start time for delivery (default: 00:00).
        preferred_delv_end_time (str): The preferred end time for delivery (default: 00:00).
    """
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('qb_user.email'))
    line1 = db.Column(db.String)
    landmark = db.Column(db.String)
    district = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    preferred_delv_start_time = db.Column(db.String, default='00:00')
    preferred_delv_end_time = db.Column(db.String, default='00:00')


# ==========================================================================================
# CreateAddress() --> Handles insertion of new address record 
# ==========================================================================================
def CreateAddress(user_email, addr_line1, land_mark, district, state, zip_code):
    """
    Creates a new address record in the database with the provided user email and address details.

    Args:
        user_email (str): The email address of the user associated with the address.
        addr_line1 (str): The first line of the address.
        land_mark (str): The landmark or additional address details.
        district (str): The district of the address.
        state (str): The state of the address.
        zip_code (str): The zip code of the address.

    This function creates a new instance of the Address model with the provided address details,
    associates it with the user's email address, and adds it to the database session. It then commits
    the changes to the database, effectively creating a new address record for the user.

    Note: This function assumes that the database session is active and the QBUser model is properly
    configured with the necessary relationship to the Address model.
    """
    
    address = Address(
        email=user_email,
        line1=addr_line1,
        landmark=land_mark,
        district=district,
        state=state,
        zip_code=zip_code
    )
    db.session.add(address)
    db.session.commit()

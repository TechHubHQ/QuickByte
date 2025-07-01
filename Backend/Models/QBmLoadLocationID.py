# =======================================================================================================
# Module for defining the CityLocation class and related functions.

# This module contains the definition of the CityLocation class, which represents city locations
# in the database. It also includes a function to create new city locations in the database.

# The CityLocation class maps to the 'city_location' table in the database.

# Functions:
#     - CreateLocationID: Creates a new city location entry in the database.

# =======================================================================================================


# ========================================================================================
# Imports/Packages
# ========================================================================================
from Backend.Connections.QBcDBConnector import db


# ======================================================================
# CityLocation Table Database schema
# ======================================================================
class CityLocation(db.Model):
    """
    Model class for representing city locations in the database.

    Attributes:
        id (int): The primary key ID of the city location.
        city (str): The name of the city.
        loc_id (int): The location ID associated with the city.
        loc_flag (bool): A flag indicating the status of the location.
    """

    __tablename__ = "city_location"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    loc_id = db.Column(db.Integer, nullable=False, unique=True)
    loc_flag = db.Column(db.Boolean, default=False)


# ===========================================================================
# CreateLocationID() --> Creates a new city location entry in the database.
# ===========================================================================
def CreateLocationID(city, loc_id, loc_flag):
    new_loc = CityLocation(city=city, loc_id=loc_id, loc_flag=loc_flag)
    db.session.add(new_loc)
    db.session.commit()

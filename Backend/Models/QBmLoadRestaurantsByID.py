# ==============================================================================================================
# Module for defining the RestaurantsByLoc class and related functions.

# This module contains the definition of the RestaurantsByLoc class, which represents restaurants
# by location in the database. It also includes a function to create new restaurant entries in the database.

# The RestaurantsByLoc class maps to the 'restaurants_by_loc' table in the database.

# Functions:
#     - CreateRestaurant: Creates a new restaurant entry in the database.

# ==============================================================================================================


# =====================================================================
# Imports/Packages
# =====================================================================
from Backend.Connections.QBcDBConnector import db


# =====================================================================
# RestaurantsByLoc table Database schema
# =====================================================================
class RestaurantsByLoc(db.Model):
    """
    Model class for representing restaurants by location in the database.

    Attributes:
        id (int): The primary key ID of the restaurant.
        location_id (int): The ID of the location where the restaurant is situated.
        restaurant_name (str): The name of the restaurant.
        num_reviews (int): The number of reviews for the restaurant.
        time_zone (str): The time zone of the restaurant.
        rating (float): The rating of the restaurant.
        ranking (int): The ranking of the restaurant.
        web_url (str): The website URL of the restaurant.
        phone (str): The phone number of the restaurant.
        email (str): The email address of the restaurant.
        address (str): The address of the restaurant.
        image_url (str): The URL of the image representing the restaurant.
        res_flag (bool): A flag indicating the status of the restaurant.
    """

    __tablename__ = 'restaurants_by_loc'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, nullable=False)
    restaurant_name = db.Column(db.String(50), nullable=False)
    num_reviews = db.Column(db.Integer, nullable=True)
    time_zone = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    web_url = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    res_flag = db.Column(db.Boolean, nullable=False)


# ============================================================================================
# CreateRestaurant() --> Creates a new restaurant entry in the database.
# ============================================================================================
def CreateRestaurant(location_id, restaurant_name, num_reviews, time_zone, rating, ranking, web_url, phone, email,
                     address, image_url, res_flag):
    """
    Creates a new restaurant entry in the database.

    Args:
        location_id (int): The ID of the location where the restaurant is situated.
        restaurant_name (str): The name of the restaurant.
        num_reviews (int): The number of reviews for the restaurant.
        time_zone (str): The time zone of the restaurant.
        rating (float): The rating of the restaurant.
        ranking (int): The ranking of the restaurant.
        web_url (str): The website URL of the restaurant.
        phone (str): The phone number of the restaurant.
        email (str): The email address of the restaurant.
        address (str): The address of the restaurant.
        image_url (str): The URL of the image representing the restaurant.
        res_flag (bool): A flag indicating the status of the restaurant.

    Returns:
        None
    """

    new_restaurant = RestaurantsByLoc(
        location_id=location_id,
        restaurant_name=restaurant_name,
        num_reviews=num_reviews,
        time_zone=time_zone,
        rating=rating,
        ranking=ranking,
        web_url=web_url,
        phone=phone,
        email=email,
        address=address,
        image_url=image_url,
        res_flag=res_flag
    )
    db.session.add(new_restaurant)
    db.session.commit()

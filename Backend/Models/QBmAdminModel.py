# ====================================================================================================================================
# This module defines the database models for restaurants and dishes, and provides functions to create new records
# in the respective tables.

# The `BizRestaurants` model represents a restaurant and includes the following fields:
# - id (int): The primary key for the restaurant.
# - restaurant_name (str): The name of the restaurant.
# - restaurant_line1 (str): The first line of the restaurant's address.
# - restaurant_city (str): The city where the restaurant is located.
# - restaurant_state (str): The state where the restaurant is located.
# - restaurant_zip (str): The zip code of the restaurant's location.
# - image_path (str): The path or URL of the restaurant's image.
# - dishes (relationship): A one-to-many relationship with the `Dishes` model, representing the dishes offered by the restaurant.

# The `Dishes` model represents a dish offered by a restaurant and includes the following fields:
# - id (int): The primary key for the dish.
# - dish_name (str): The name of the dish.
# - dish_price (int): The price of the dish.
# - dish_image (str): The path or URL of the dish's image.
# - restaurant_id (int): The foreign key referencing the `BizRestaurants` model, indicating the restaurant that offers this dish.

# The module also provides two functions:
# 1. `CreateRestaurant`: Creates a new restaurant record with the provided details.
# 2. `CreateDish`: Creates a new dish record with the provided details and associates it with the specified restaurant.

# This module should be imported and used in conjunction with the SQLAlchemy database connection to manage restaurant
# and dish data in the application.
# ==================================================================================================================================


# ==========================================================================
# Imports/Packages
# ==========================================================================
from Backend.Connections.QBcDBConnector import db


# ==========================================================================
# BizRestaurants Table DataBase schema
# ==========================================================================
class BizRestaurants(db.model):
    """
    This class represents the BizRestaurants model for storing restaurant information.

    Attributes:
        id (int): The primary key for the restaurant.
        restaurant_name (str): The name of the restaurant.
        restaurant_line1 (str): The first line of the restaurant's address.
        restaurant_city (str): The city where the restaurant is located.
        restaurant_state (str): The state where the restaurant is located.
        restaurant_zip (str): The zip code of the restaurant's location.
        image_path (str): The path or URL of the restaurant's image.
        dishes (relationship): A one-to-many relationship with the `Dishes` model, representing the dishes offered by the restaurant.
    """
    
    __tablename__ = 'biz_restaurants'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)
    restaurant_line1 = db.Column(db.String(100), nullable=False)
    restaurant_city = db.Column(db.String(100), nullable=False)
    restaurant_state = db.Column(db.String(100), nullable=False)
    restaurant_zip = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    dishes = db.relationship('Dishes', backref='restaurant', lazy=True)


# ============================================================================
# Dishes Table DataBase schema
# ============================================================================
class Dishes(db.model):
    """
    This class represents the Dishes model for storing dish information.

    Attributes:
        id (int): The primary key for the dish.
        dish_name (str): The name of the dish.
        dish_price (int): The price of the dish.
        dish_image (str): The path or URL of the dish's image.
        restaurant_id (int): The foreign key referencing the `BizRestaurants` model, indicating the restaurant that offers this dish.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100), nullable=False)
    dish_price = db.Column(db.Integer, nullable=False)
    dish_image = db.Column(db.String(100), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


# ==============================================================================================
# CreateRestaurant() --> Handles insertion of new restaurant record in database.
# ==============================================================================================
def CreateRestaurant(restaurant_name, restaurant_line1, restaurant_city, restaurant_state, restaurant_zip, image_path):
    """
    Creates a new restaurant record in the database with the provided details.

    Args:
        restaurant_name (str): The name of the restaurant.
        restaurant_line1 (str): The first line of the restaurant's address.
        restaurant_city (str): The city where the restaurant is located.
        restaurant_state (str): The state where the restaurant is located.
        restaurant_zip (str): The zip code of the restaurant's location.
        image_path (str): The path or URL of the restaurant's image.

    Returns:
        int: The ID of the newly created restaurant record.

    This function creates a new instance of the `BizRestaurants` model with the provided details, adds it to the
    database session, and commits the changes to the database. It returns the ID of the newly created restaurant record.
    """
    
    restaurant = BizRestaurants(
        restaurant_name=restaurant_name,
        restaurant_line1=restaurant_line1,
        restaurant_city=restaurant_city,
        restaurant_state=restaurant_state,
        restaurant_zip=restaurant_zip,
        image_path=image_path
    )
    db.session.add(restaurant)
    db.session.commit()
    return restaurant.id


# ====================================================================================================
# CreateDish() --> Handles insertion of new dish record in database.
# ====================================================================================================
def CreateDish(dish_name, dish_description, dish_price, dish_image, restaurant_id):
    """
    Creates a new dish record in the database with the provided details and associates it with the specified restaurant.

    Args:
        dish_name (str): The name of the dish.
        dish_description (str): The description of the dish.
        dish_price (int): The price of the dish.
        dish_image (str): The path or URL of the dish's image.
        restaurant_id (int): The ID of the restaurant that offers this dish.

    Returns:
        int: The ID of the newly created dish record.

    This function creates a new instance of the `Dishes` model with the provided details, associates it with the
    restaurant specified by the `restaurant_id`, adds it to the database session, and commits the changes to the
    database. It returns the ID of the newly created dish record.
    """
    
    dish = Dishes(
        dish_name=dish_name,
        dish_description=dish_description,
        dish_price=dish_price,
        dish_image=dish_image,
        restaurant_id=restaurant_id
    )
    db.session.add(dish)
    db.session.commit()
    return dish.id

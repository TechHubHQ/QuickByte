# ======================================================================================================
# Module for defining the MenuDetails class and related functions.

# This module contains the definition of the MenuDetails class, which represents menu items
# in the database. It also includes a function to create new menu items in the database.

# The MenuDetails class maps to the 'menu_details' table in the database.

# Functions:
#     - CreateMenu: Creates a new menu item entry in the database.

# ======================================================================================================


# ======================================================================
# Imports/Packages
# ======================================================================
from Backend.Connections.QBcDBConnector import db


# ======================================================================
# MenuDetails Table Database schema
# ======================================================================
class MenuDetails(db.Model):
    """
    Model class for representing menu items in the database.

    Attributes:
        id (int): The primary key ID of the menu item.
        cuisine_name (str): The name of the cuisine.
        item_category (str): The category of the menu item.
        item_name (str): The name of the menu item.
        item_type (str): The type of the menu item.
        item_price (float): The price of the menu item.
        item_description (str): The description of the menu item.
        item_reviews (int): The number of reviews for the menu item.
        item_flag (bool): A flag indicating the status of the menu item.
    """
    
    __tablename__ = 'menu_details'
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(db.String(50), nullable=False)
    item_category = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_description = db.Column(db.String(200), nullable=False)
    item_reviews = db.Column(db.Integer, nullable=True)
    item_flag = db.Column(db.Boolean, nullable=False)


# =====================================================================================
# CreateMenu() --> Creates a new menu item entry in the database.
# =====================================================================================
def CreateMenu(cuisine_name, item_category, item_name, item_type, item_price, item_description,
               item_reviews, item_flag):
    """
    Creates a new menu item entry in the database.

    Args:
        cuisine_name (str): The name of the cuisine.
        item_category (str): The category of the menu item.
        item_name (str): The name of the menu item.
        item_type (str): The type of the menu item.
        item_price (float): The price of the menu item.
        item_description (str): The description of the menu item.
        item_reviews (int): The number of reviews for the menu item.
        item_flag (bool): A flag indicating the status of the menu item.

    Returns:
        None
    """
    
    new_menu = MenuDetails(cuisine_name=cuisine_name,
                           item_category=item_category,
                           item_name=item_name,
                           item_type=item_type,
                           item_price=item_price,
                           item_description=item_description,
                           item_reviews=item_reviews,
                           item_flag=item_flag)
    db.session.add(new_menu)
    db.session.commit()

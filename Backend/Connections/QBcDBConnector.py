# ========================================================================================================================
# This module sets up the database connection and initialization for the Flask application using SQLAlchemy and Bcrypt.

# It provides the following functionality:

# 1. Initializes an instance of SQLAlchemy (db) and Bcrypt (bcrypt).
# 2. Defines the `init_db` function to configure the database connection settings and initialize the database and Bcrypt
#    with the Flask application.

# This module is typically imported and used in the main application setup to handle the database connection and
# encryption utilities.
# ========================================================================================================================

# ========================================================
# Imports/Packages
# ========================================================

import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


# ================================================================
# init_db() --> Initializes DB connections
# ================================================================

def init_db(app):
    """
    Initializes the database connection and encryption utilities for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    This function performs the following tasks:
    1. Constructs the path to the SQLite database file ('QB.db') located in the 'DataBase' directory.
    2. Configures the SQLAlchemy database URI and other settings in the Flask app's configuration.
    3. Initializes the SQLAlchemy instance (db) with the Flask app.
    4. Initializes the Bcrypt instance (bcrypt) with the Flask app.
    5. Creates all database tables defined in the application models within the app context.

    This function should be called during the application setup to ensure the database connection and encryption
    utilities are properly initialized before handling any requests.
    """
    
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'DataBase', 'QB.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'QuickBytePassKey'

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

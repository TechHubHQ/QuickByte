# ==========================================================================================================================
# This module defines the Configuration class for the application, which loads environment variables
# from a .env file and provides access to various configuration settings.

# The Configuration class includes the following properties:

# - DB: The database connection string or URI.
# - SECRET_KEY: The secret key used for securing the application's sessions.
# - UPLOAD_FOLDER_RELATIVE: The relative path for the folder where user-uploaded files (e.g., images) are stored.
# - QR_FOLDER_RELATIVE: The relative path for the folder where QR codes are stored.
# - APP_LOG_FOLDER: The directory path for storing application logs.
# - INTEGRATION_LOG_FOLDER: The directory path for storing integration logs.
# - LOGIC_LOG_FOLDER: The directory path for storing logic logs.
# - SERVICES_LOG_FOLDER: The directory path for storing service logs.
# - APP_LOG_FILE: The file path for the application log file, which includes the current date in the filename.

# This module is typically imported and used in the main application setup to configure the application
# with the desired settings based on the environment variables defined in the .env file.
# ==========================================================================================================================


# ======================================================================
# Imports/Packages
# ======================================================================
import os
from dotenv import load_dotenv
from datetime import datetime

script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

current_date = datetime.now().strftime("%Y-%m-%d")

# ====================================================================
# Config --> Configuration for QB App.
# ====================================================================
class Config:
    """
    This class provides access to various configuration settings for the application.

    The configuration settings are loaded from environment variables defined in a .env file.
    The class properties provide access to settings such as the database connection string,
    secret key, upload folder paths, log folder paths, and the application log file path.

    This class is intended to be used during the application setup to configure the application
    with the desired settings based on the defined environment variables.
    """
    
    DB = os.environ.get('DB')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER_RELATIVE = os.environ.get('UPLOAD_FOLDER_RELATIVE')
    QR_FOLDER_RELATIVE = os.environ.get('QRCODE_FOLDER_RELATIVE')
    APP_LOG_FOLDER = os.environ.get('APP_LOG_DIR')
    INTEGRATION_LOG_FOLDER = os.environ.get('INTEGRATION_LOG_DIR')
    LOGIC_LOG_FOLDER = os.environ.get('LOGIC_LOG_DIR')
    SERVICES_LOG_FOLDER = os.environ.get('SERVICES_LOG_DIR')
    APP_LOG_FILE = f"{APP_LOG_FOLDER}/{current_date}_QUICK-BYTE.log"

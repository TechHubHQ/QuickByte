# ===========================================================================================================================
# This module provides a UserController class with static methods for handling user-related operations such as
# image upload,
# password update, notification preference update, and delivery address update.

# The UserController class uses various models and database connections defined in other modules to perform
# the required operations. It interacts with the QBUser, Address, and NotificationControl models to update user data,
# preferences, and delivery details.

# The module also imports the necessary libraries and utilities, including os for file handling, secure_filename for
# secure file naming, and current_app from Flask for accessing the application configuration.
# ==========================================================================================================================


# =======================================================
# Imports/Packages
# =======================================================
import os
from werkzeug.utils import secure_filename
from flask import current_app
from Backend.Models.QBmUserModel import QBUser
from Backend.Models.QBmAddressModel import Address
from Backend.Models.QBmNotificationModel import NotificationControl
from Backend.Connections.QBcDBConnector import db, bcrypt


# ===============================================================
# UserController --> Controls User Transactions 
# ===============================================================

class UserController:
    """
    This class provides static methods for handling user-related operations such as image upload, password update,
    notification preference update, and delivery address update.
    """

    # ========================================================================================================
    # SaveImage() --> saves the image file to the upload folder with a secure filename based on the username.
    # ========================================================================================================
    @staticmethod
    def SaveImage(username, image_file):
        """
        Saves the provided image file with a secure filename based on the username.

        Args:
            username (str): The username of the user.
            image_file (FileStorage): The FileStorage object containing the image file.

        This method securely constructs a new filename based on the username, saves the image file to the configured
        upload folder, and prints a message indicating the file path. If no image file is provided, it prints a message
        indicating that no image was selected.
        """

        if image_file:
            original_file = secure_filename(image_file.filename)
            file_extension = original_file.split(".")[-1]
            username = username.replace(" ", "_")
            new_file = f"{username}.{file_extension}"
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_file))
            print(f"Image saved to {current_app.config['UPLOAD_FOLDER']}")
        else:
            print("No image selected")

    # ============================================================================================================
    # UpdateUser() --> Updates the password for the specified user with a hashed version of the provided password.
    # ============================================================================================================        
    @staticmethod
    def UpdateUser(username, password):
        """
        Updates the password for the specified user with a hashed version of the provided password.

        Args:
            username (str): The username of the user.
            password (str): The new password to be set.

        This method generates a hashed version of the provided password using bcrypt and updates the password
        for the user with the specified username in the QBUser model. It then commits the changes to the database.
        """

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        QBUser.query.filter_by(username=username).update({"password": hashed_password})
        db.session.commit()

    # ===================================================================================
    # UpdatePreferences() --> Updates the notification preference for the specified user.
    # ===================================================================================
    @staticmethod
    def UpdatePreferences(username, flag):
        """
        Updates the notification preference for the specified user.

        Args:
            username (str): The username of the user.
            flag (bool): The notification preference flag (True or False).

        This method updates the notify_flag value in the NotificationControl model for the specified user.
        If the user does not exist in the model, it creates a new record with the provided username and flag.
        If the user exists, it updates the notify_flag value for that user. It then commits the changes to the database.
        """

        user = NotificationControl.query.filter_by(username=username).first()
        if user is None:
            user = NotificationControl(username=username, notify_flag=flag)
            db.session.add(user)
            db.session.commit()
        else:
            NotificationControl.query.filter_by(username=username).update({"notify_flag": flag})
            db.session.commit()

    # ======================================================================================================
    # UpdateDelivery() --> Updates the delivery address and preferred delivery time for the specified user.
    # ======================================================================================================
    @staticmethod
    def UpdateDelivery(email, line1, landmark, state, district, preferred_delv_start_time, preferred_delv_end_time):
        """
        Updates the delivery address and preferred delivery time for the specified user.

        Args:
            email (str): The email address of the user.
            line1 (str): The first line of the delivery address.
            landmark (str): The landmark for the delivery address.
            state (str): The state for the delivery address.
            district (str): The district for the delivery address.
            preferred_delv_start_time (datetime): The preferred start time for delivery.
            preferred_delv_end_time (datetime): The preferred end time for delivery.

        This method updates the delivery address and preferred delivery time for the user with the specified
        email address in the Address model.
        It then commits the changes to the database.
        """

        Address.query.filter_by(email=email).update({
            "line1": line1,
            "landmark": landmark,
            "state": state,
            "district": district,
            "preferred_delv_start_time": preferred_delv_start_time,
            "preferred_delv_end_time": preferred_delv_end_time
        })
        db.session.commit()

# ==========================================================================================
# Module for defining the NotificationControl class.

# This module contains the definition of the NotificationControl class, which represents
# the notification control table schema in the database.

# The NotificationControl class maps to the 'notification_control' table in the database.

# =========================================================================================


# =====================================================================
# Imports/Packages
# =====================================================================
from Backend.Connections.QBcDBConnector import db


# ==================================================
# Notification control table schema
# ==================================================
class NotificationControl(db.Model):
    """
    Model class for representing the notification control table schema in the database.

    Attributes:
        id (int): The primary key ID of the notification control entry.
        username (str): The username associated with the notification control.
        notify_flag (bool): A flag indicating whether notifications are enabled or not.
        inserted_at (datetime): The datetime when the entry was inserted into the database.
        last_updated (datetime): The datetime when the entry was last updated in the database.
        last_notified (datetime): The datetime of the last notification.

    """
    
    __tablename__ = 'notification_control'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    notify_flag = db.Column(db.Boolean, default=True)
    inserted_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    last_notified = db.Column(db.DateTime)

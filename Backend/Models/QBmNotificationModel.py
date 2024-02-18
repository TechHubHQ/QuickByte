from datetime import datetime
from Backend.Connections.QBcDBConnector import db


# Notification control table schema
class NotificationControl(db.Model):
    __tablename__ = 'notification_control'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    notify_flag = db.Column(db.Boolean, default=True)
    inserted_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    last_notified = db.Column(db.DateTime)

# ==========================================================================
# Imports/Packages
# ==========================================================================
from pytz import timezone
from datetime import datetime
from Backend.Connections.QBcDBConnector import db


class QBBiz(db.model):
    __tablename__ = 'QB_BIZ'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    ist = timezone('Asia/Kolkata')
    registered_on = db.Column(db.DateTime, default=datetime.now(ist))

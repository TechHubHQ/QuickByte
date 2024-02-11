# /backend/QBcDBConnector.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
bcrypt = Bcrypt()


def init_db(app):
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'DataBase', 'QB.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'QuickBytePassKey'

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

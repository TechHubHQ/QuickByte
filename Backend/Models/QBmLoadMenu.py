from Backend.Connections.QBcDBConnector import db


class RestMenu(db.Model):
    __tablename__ = 'rest_menu'
    id = db.Column(db.Integer, primary_key=True)


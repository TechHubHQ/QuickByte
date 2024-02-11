from Backend.Connections.QBcDBConnector import db


class CityLocation(db.Model):
    __tablename__ = "city_location"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    loc_id = db.Column(db.Integer, nullable=False, unique=True)
    loc_flag = db.Column(db.Boolean, default=False)


def CreateLocationID(city, loc_id, loc_flag):
    new_loc = CityLocation(city=city, loc_id=loc_id, loc_flag=loc_flag)
    db.session.add(new_loc)
    db.session.commit()

from Backend.Connections.QBcDBConnector import db


# Address Table DataBase Schema
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('qb_user.email'))
    line1 = db.Column(db.String)
    landmark = db.Column(db.String)
    district = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    preferred_delv_start_time = db.Column(db.String, default='00:00')
    preferred_delv_end_time = db.Column(db.String, default='00:00')


def CreateAddress(user_email, addr_line1, land_mark, district, state, zip_code):
    address = Address(
        email=user_email,
        line1=addr_line1,
        landmark=land_mark,
        district=district,
        state=state,
        zip_code=zip_code
    )
    db.session.add(address)
    db.session.commit()

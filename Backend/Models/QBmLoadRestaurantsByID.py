from Backend.Connections.QBcDBConnector import db


class RestaurantsByLoc(db.Model):
    __tablename__ = 'restaurants_by_loc'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, nullable=False)
    restaurant_name = db.Column(db.String(50), nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)
    time_zone = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    web_url = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200), nullable=False)
    res_flag = db.Column(db.Boolean, nullable=False)


def CreateRestaurant(location_id, restaurant_name, num_reviews, time_zone, rating, ranking, web_url, phone, email,
                     address, res_flag):
    new_restaurant = RestaurantsByLoc(
        location_id=location_id,
        restaurant_name=restaurant_name,
        num_reviews=num_reviews,
        time_zone=time_zone,
        rating=rating,
        ranking=ranking,
        web_url=web_url,
        phone=phone,
        email=email,
        address=address,
        res_flag=res_flag
    )
    db.session.add(new_restaurant)
    db.session.commit()

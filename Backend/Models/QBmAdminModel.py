from Backend.Connections.QBcDBConnector import db


# Restaurants Table DataBase schema
class BizRestaurants(db.model):
    __tablename__ = 'biz_restaurants'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)
    restaurant_line1 = db.Column(db.String(100), nullable=False)
    restaurant_city = db.Column(db.String(100), nullable=False)
    restaurant_state = db.Column(db.String(100), nullable=False)
    restaurant_zip = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    dishes = db.relationship('Dishes', backref='restaurant', lazy=True)


# Dishes Table DataBase schema
class Dishes(db.model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100), nullable=False)
    dish_price = db.Column(db.Integer, nullable=False)
    dish_image = db.Column(db.String(100), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


def CreateRestaurant(restaurant_name, restaurant_line1, restaurant_city, restaurant_state, restaurant_zip, image_path):
    restaurant = BizRestaurants(
        restaurant_name=restaurant_name,
        restaurant_line1=restaurant_line1,
        restaurant_city=restaurant_city,
        restaurant_state=restaurant_state,
        restaurant_zip=restaurant_zip,
        image_path=image_path
    )
    db.session.add(restaurant)
    db.session.commit()
    return restaurant.id


def CreateDish(dish_name, dish_description, dish_price, dish_image, restaurant_id):
    dish = Dishes(
        dish_name=dish_name,
        dish_description=dish_description,
        dish_price=dish_price,
        dish_image=dish_image,
        restaurant_id=restaurant_id
    )
    db.session.add(dish)
    db.session.commit()
    return dish.id

from Backend.Connections.QBcDBConnector import db


class MenuDetails(db.Model):
    __tablename__ = 'menu_details'
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(db.String(50), nullable=False)
    item_category = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_description = db.Column(db.String(200), nullable=False)
    item_reviews = db.Column(db.Integer, nullable=True)
    item_flag = db.Column(db.Boolean, nullable=False)


def CreateMenu(cuisine_name, item_category, item_name, item_type, item_price, item_description,
               item_reviews, item_flag):
    new_menu = MenuDetails(cuisine_name=cuisine_name,
                           item_category=item_category,
                           item_name=item_name,
                           item_type=item_type,
                           item_price=item_price,
                           item_description=item_description,
                           item_reviews=item_reviews,
                           item_flag=item_flag)
    db.session.add(new_menu)
    db.session.commit()
    print(f"Item created successfully --> {item_name}")

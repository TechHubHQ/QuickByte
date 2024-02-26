import os
import sys
import json
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from Backend.Connections.QBcDBConnector import db
from Backend.Models.QBmLoadMenu import MenuDetails, CreateMenu

app.app_context().push()
db.create_all()

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file
json_file = os.path.join(current_dir, "Data", "FoodMenu.json")


def GetFoodMenu():
    with open(json_file, "r") as f:
        return json.load(f)


def CreateFoodMenu():
    print(f"Creating food menu...")
    food_menu = GetFoodMenu()
    menu = food_menu["menu"]
    menu_details = MenuDetails.query.first()
    if menu_details is not None:
        item_flag = menu_details.item_flag
    else:
        item_flag = None
    print(f"Menu details: {menu_details}")

    if item_flag is None:
        item_flag = True

    for cuisine in menu:
        cuisine_name = cuisine["cuisine"]
        categories = cuisine["categories"]
        for category in categories:
            item_category = category["name"]
            items = category["items"]
            print("\n------------------------------------------------------------------")
            print(f"Items under new cuisine: {cuisine_name}, {item_category}")
            print("------------------------------------------------------------------\n")
            for item in items:
                item_name = item["name"]
                item_type = item["type"]
                item_price = item["price"]
                item_description = item["description"]
                item_reviews = item["rating"]

                # Check if item with same name already exists in the database
                existing_item = MenuDetails.query.filter_by(item_name=item_name).first()
                if existing_item is None:
                    CreateMenu(
                        cuisine_name=cuisine_name,
                        item_category=item_category,
                        item_name=item_name,
                        item_type=item_type,
                        item_price=item_price,
                        item_description=item_description,
                        item_reviews=item_reviews,
                        item_flag=item_flag
                    )
                else:
                    print(f"Item with name '{item_name}' already exists in database. Skipping insertion.")


CreateFoodMenu()

import os
import sys
import requests
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from dotenv import load_dotenv
from Backend.Models.QBmLoadRestaurantsByID import CreateRestaurant, RestaurantsByLoc
from Backend.Models.QBmLoadLocationID import CityLocation
from Backend.Connections.QBcDBConnector import db

script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'config', '.env')

load_dotenv(env_path)
app.app_context().push()
db.create_all()

url = os.environ.get('REST_API')

headers = {
    "X-RapidAPI-Key": os.environ.get('REST_API_KEY'),
    "X-RapidAPI-Host": os.environ.get('REST_API_HOST')
}

city_ids = CityLocation.query.with_entities(CityLocation.loc_id).distinct().all()
loc_ids = [city_id[0] for city_id in city_ids]
print(loc_ids)

for loc_id in loc_ids:
    print(loc_id)
    querystring = {"location_id": loc_id}
    response = requests.get(url, headers=headers, params=querystring)
    tmpResArr = response.json().get('data', [])

    for res in tmpResArr:
        # Check if the restaurant already exists in the database
        existing_restaurant = RestaurantsByLoc.query.filter_by(location_id=loc_id).first()
        if existing_restaurant:
            print(f"Restaurant already exists in the database: loc_id --> {res['location_id']}")
            continue  # Skip this restaurant if it already exists in the database

        res_flag = None  # Initialize res_flag to None

        # Check if res_flag is NULL or 0
        if res_flag is None or res_flag == 0:
            print(res_flag)
            if None in (
                    res.get('location_id'), res.get('name')):
                print(f"Skipping this restaurant {res.get('location_id')} or {res.get('name')} field is None")
                continue  # Skip this restaurant if any required field is None

            print("\n----------------------------------------------------------")
            print("New Restaurant -- registration: ")
            print("----------------------------------------------------------\n")
            print(res.get('location_id'))
            print(res.get('name'))
            print(res.get('num_reviews'))
            print(res.get('timezone'))
            print(res.get('rating'))
            print(res.get('ranking'))
            print(res.get('web_url'))
            print(res.get('phone'))
            print(res.get('email'))
            address_obj = res.get('address_obj')
            if address_obj:
                address = address_obj.get('street1', 'Unknown Address')
                city = address_obj.get('city', 'Unknown')
                state = address_obj.get('state', 'Unknown')
                country = address_obj.get('country', 'Unknown')
                postal_code = address_obj.get('postal_code', 'Unknown')
                full_address = f"{address}, {city}, {state}, {country}, {postal_code}"
            else:
                full_address = 'Unknown Address'
            print(full_address)

            location_id = res.get('location_id')
            restaurant_name = res.get('name')
            num_reviews = res.get('num_reviews')
            time_zone = res.get('timezone')
            rating = res.get('rating')
            ranking = res.get('ranking')
            web_url = res.get('web_url')
            phone = res.get('phone')
            email = res.get('email')
            res_flag = True
            CreateRestaurant(location_id, restaurant_name, num_reviews, time_zone, rating, ranking, web_url, phone,
                             email, full_address, res_flag)

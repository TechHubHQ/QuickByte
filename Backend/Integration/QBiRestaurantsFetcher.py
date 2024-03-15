# ============================================================================================================================
# This script fetches restaurant data from a third-party API and stores it in the database. It performs the following tasks:

# 1. Sets up logging and loads environment variables from a .env file.
# 2. Adds the root directory to the system path and imports necessary modules.
# 3. Initializes the Flask application context and creates the database tables if they don't exist.
# 4. Retrieves the API URL and headers from environment variables.
# 5. Fetches a list of distinct city IDs from the database.
# 6. Iterates over each city ID and sends a request to the API to fetch restaurant data for that location.
# 7. For each restaurant in the API response:
#     a. Checks if the restaurant already exists in the database.
#     b. If the restaurant doesn't exist, it extracts relevant data from the API response.
#     c. Logs the extracted restaurant data.
#     d. Creates a new record in the database with the restaurant data.

# This script is designed to be run periodically or on-demand to keep the restaurant data in the database up-to-date.
# ==========================================================================================================================


# ==================================================
# Imports/packages
# ==================================================

import os
import sys
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
INTEGRATION_LOG_DIR = os.environ.get("INTEGRATION_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=os.path.join(INTEGRATION_LOG_DIR, f'{current_date}_RestaurantsFetcher.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app

from Backend.Models.QBmLoadRestaurantsByID import CreateRestaurant, RestaurantsByLoc
from Backend.Models.QBmLoadLocationID import CityLocation
from Backend.Connections.QBcDBConnector import db

app.app_context().push()
db.create_all()

url = os.environ.get('REST_API')

headers = {
    "X-RapidAPI-Key": os.environ.get('REST_API_KEY'),
    "X-RapidAPI-Host": os.environ.get('REST_API_HOST')
}

city_ids = CityLocation.query.with_entities(CityLocation.loc_id).distinct().all()
loc_ids = [city_id[0] for city_id in city_ids]
logging.info(f"City IDs: {loc_ids}")

for loc_id in loc_ids:
    logging.info(f"Processing location ID: {loc_id}")
    querystring = {"location_id": loc_id}
    response = requests.get(url, headers=headers, params=querystring)
    tmpResArr = response.json().get('data', [])

    for res in tmpResArr:
        # Check if the restaurant already exists in the database
        existing_restaurant = RestaurantsByLoc.query.filter_by(location_id=loc_id).first()
        if existing_restaurant:
            logging.info(f"Restaurant already exists in the database: loc_id --> {res['location_id']}")
            continue  # Skip this restaurant if it already exists in the database

        res_flag = None  # Initialize res_flag to None

        # Check if res_flag is NULL or 0
        if res_flag is None or res_flag == 0:
            logging.info(res_flag)
            if None in (
                    res.get('location_id'), res.get('name')):
                logging.info(f"Skipping this restaurant {res.get('location_id')} or {res.get('name')} field is None")
                continue  # Skip this restaurant if any required field is None

            logging.info("------------------------------------------------------------")
            logging.info("New Restaurant -- registration: ")
            logging.info("----------------------------------------------------------\n")
            logging.info(res.get('location_id'))
            logging.info(res.get('name'))
            logging.info(res.get('num_reviews'))
            logging.info(res.get('timezone'))
            logging.info(res.get('rating'))
            logging.info(res.get('ranking'))
            logging.info(res.get('web_url'))
            logging.info(res.get('phone'))
            logging.info(res.get('email'))
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
            logging.info(full_address)

            # Get the small photo URL
            photo = res.get('photo')
            if photo:
                image_url = photo.get('images', {}).get('original', {}).get('url')
                logging.info(image_url)
            else:
                image_url = 'None'

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
                             email, full_address, image_url, res_flag)

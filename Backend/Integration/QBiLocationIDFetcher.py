import os
import requests
import sys
from dotenv import load_dotenv
import logging
from datetime import datetime

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
INTEGRATION_LOG_DIR = os.environ.get("INTEGRATION_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=os.path.join(INTEGRATION_LOG_DIR, f'{current_date}_LocationIDFetcher.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from Backend.Models.QBmLoadLocationID import CityLocation, CreateLocationID
from Backend.Models.QBmAddressModel import Address
from Backend.Connections.QBcDBConnector import db

app.app_context().push()
db.create_all()

url = os.environ.get('LOC_API')

headers = {
    "X-RapidAPI-Key": os.environ.get('LOC_API_KEY'),
    "X-RapidAPI-Host": os.environ.get('LOC_API_HOST')
}

cities_list = Address.query.with_entities(Address.district).distinct().all()
cities = [city[0] for city in cities_list]

for city in cities:
    querystring = {"query": city}

    response = requests.get(url, headers=headers, params=querystring)

    tmpArr = response.json()
    tmpLocArr = tmpArr.get('data', [])
    CityLoc = CityLocation.query.filter_by(city=city).first()
    loc_flag = None
    for loc in tmpLocArr:
        loc_id = loc.get('result_object', {}).get('location_id')
        if not loc_flag:
            name = loc.get('result_object', {}).get('name')
            logging.info(f"Processing location: {name}, ID: {loc_id}, City: {city}")
            existing_loc = CityLocation.query.filter_by(loc_id=loc_id).first()

            if not existing_loc and not loc_flag:
                loc_flag = True
                CreateLocationID(city=city, loc_id=loc_id, loc_flag=loc_flag)
                logging.info("-----------------------------------------------------------")
                logging.info(f"New Location committed to DB --> ID: {loc_id} City: {city}")
                logging.info("---------------------------------------------------------\n")

        else:
            logging.info(f"Location already exists")
            break

    logging.info(f"City: {city} completed")

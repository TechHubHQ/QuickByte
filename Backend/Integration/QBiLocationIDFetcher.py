import os
import requests
import sys
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from dotenv import load_dotenv
from Backend.Models.QBmLoadLocationID import CityLocation, CreateLocationID
from Backend.Models.QBmAddressModel import Address
from Backend.Connections.QBcDBConnector import db

script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'config', '.env')

load_dotenv(env_path)
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
            print(loc_id, city)
            existing_loc = CityLocation.query.filter_by(loc_id=loc_id).first()

            if not existing_loc and not loc_flag:
                loc_flag = True
                CreateLocationID(city=city, loc_id=loc_id, loc_flag=loc_flag)
                print("\n---------------------------------------------------------")
                print(f"New Location committed to DB --> ID: {loc_id} City: {city}")
                print("---------------------------------------------------------\n")

        else:
            print(f"Location already exists")
            break

    print(f"City: {city} completed")

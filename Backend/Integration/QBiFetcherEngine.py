import os
import sys
import requests
import logging
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from Backend.Models.QBmLoadLocationID import CreateLocationID
from dotenv import load_dotenv
from datetime import datetime
from Backend.Connections.QBcDBConnector import db

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'config', '.env')
load_dotenv(env_path)
INTEGRATION_LOG_DIR = os.environ.get("INTEGRATION_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=os.path.join(INTEGRATION_LOG_DIR, f'{current_date}_FetchALLEngine.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app.app_context().push()
db.create_all()


def fetch_location_ids_for_indian_cities():
    url = "https://travel-advisor.p.rapidapi.com/locations/search"
    headers = {
        "X-RapidAPI-Key": "897b3eccc5msh07c09ba21aae956p1040b7jsnbdaeb583f509",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    andhra_telangana = [
        # Andhra Pradesh
        "Anantapur",
        "Chitoor",
        "East Godavari",
        "Guntur",
        "Krishna",
        "Kurnool",
        "Nellore",
        "Prakasam",
        "Srikakulam",
        "Visakhapatnam",
        "Vizianagaram",
        "West Godavari",
        # Telangana
        "Adilabad",
        "Bhadradri Kothagudem",
        "Hyderabad",
        "Jagtial",
        "Jangoan",
        "Jayashankar Bhupalapally",
        "Jogulamba Gadwal",
        "Kamareddy",
        "Karimnagar",
        "Khammam",
        "Komaram Bheem Asifabad",
        "Mahabubabad"
        "Mahbubnagar",
        "Mancherial",
        "Medak",
        "Medchal",
        "Nagarkurnool",
        "Nalgonda",
        "Nirmal",
        "Nizamabad",
        "Peddapalli",
        "Rajanna Sircilla",
        "Rangareddy",
        "Sangareddy",
        "Siddipet",
        "Suryapet",
        "Vikarabad",
        "Wanaparthy",
        "Warangal Rural",
        "Warangal Urban"
        "Yadadri Bhuvanagiri"
    ]

    location_ids = {}

    for city in andhra_telangana:
        querystring = {"query": city}
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise HTTPError for bad responses
            json_data = response.json()

            # Extract the first location ID for the city
            first_location_id = json_data.get('data', [])[0].get('result_object', {}).get('location_id', None)

            if first_location_id:
                location_ids[city] = first_location_id
                logging.info(f"Location ID for {city}: {first_location_id}")
                CreateLocationID(city, first_location_id, True)
        except Exception as e:
            logging.error(f"An error occurred while fetching data for {city}: {e}")

    return location_ids


if __name__ == "__main__":
    indian_city_location_ids = fetch_location_ids_for_indian_cities()
    print(indian_city_location_ids)

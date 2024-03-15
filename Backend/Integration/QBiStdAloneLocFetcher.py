# =============================================================================================================================
# This script fetches location IDs for cities in the Andhra Pradesh and Telangana states of India from a third-party API
# and stores them in a database. It performs the following tasks:

# 1. Sets up logging and loads environment variables from a .env file.
# 2. Adds the root directory to the system path and imports necessary modules.
# 3. Initializes the Flask application context and creates the database tables if they don't exist.
# 4. Defines a list of cities in Andhra Pradesh and Telangana for which location IDs need to be fetched.
# 5. The `fetch_location_ids_for_indian_cities` function:
#     a. Retrieves the API URL and headers from environment variables.
#     b. Iterates over the list of cities.
#     c. For each city, sends a request to the API to fetch the location ID.
#     d. Extracts the first location ID from the API response.
#     e. Stores the location ID and city in a dictionary and logs it.
#     f. Creates a new record in the database with the city name, location ID, and a flag indicating it's an Indian city.
#     g. Handles and logs any exceptions that occur during the API request or data processing.
# 6. If the script is run directly, it calls the `fetch_location_ids_for_indian_cities` function and prints the
#    dictionary of location IDs.

# This script is designed to be run periodically or on-demand to fetch and store location IDs for cities in Andhra
# Pradesh and Telangana, which can be used for further processing or integration with other systems.
# =============================================================================================================================


# ====================================================
# Imports/Packages
# ====================================================

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
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
INTEGRATION_LOG_DIR = os.environ.get("INTEGRATION_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=os.path.join(INTEGRATION_LOG_DIR, f'{current_date}_FetchALLEngine.log'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app.app_context().push()
db.create_all()


# =========================================================================================================
# FetchLocationIDS --> fetches location ids for cities in AP and TN states of India from a third-party API
# =========================================================================================================

def FetchLocationIDS():
    """
    Fetches location IDs for cities in the Andhra Pradesh and Telangana states of India from a third-party API.

    Returns:
        dict: A dictionary mapping city names to their corresponding location IDs.

    This function iterates over a predefined list of cities in Andhra Pradesh and Telangana, sends a request to
    the API to fetch the location ID for each city, and stores the location ID and city name in a dictionary.
    It also creates a new record in the database with the city name, location ID, and a flag indicating it's an
    Indian city.

    If an exception occurs while fetching data for a city, it logs an error message and continues with the next city.
    """
    
    url = os.environ.get("LOC_API")
    headers = {
        "X-RapidAPI-Key": os.environ.get("LOC_API_KEY"),
        "X-RapidAPI-Host": os.environ.get("LOC_API_HOST")
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
    indian_city_location_ids = FetchLocationIDS()
    print(indian_city_location_ids)

import requests
from app import app
from Backend.Models.QBmLoadLocationID import CityLocation, CreateLocationID
from Backend.Models.QBmLoadAddress import Address
from Backend.Connections.QBcDBConnector import db

app.app_context().push()
db.create_all()

url = "https://travel-advisor.p.rapidapi.com/locations/search"

headers = {
    "X-RapidAPI-Key": "897b3eccc5msh07c09ba21aae956p1040b7jsnbdaeb583f509",
    "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}

cities_list = Address.query.with_entities(Address.city).distinct().all()
cities = [city[0] for city in cities_list]

for city in cities:
    querystring = {"query": city}

    response = requests.get(url, headers=headers, params=querystring)

    tmpArr = response.json()
    tmpLocArr = tmpArr.get('data', [])
    loc_flag = CityLocation.query.filter_by(city=city).first()
    for loc in tmpLocArr:
        if not loc_flag:
            loc_id = loc.get('result_object', {}).get('location_id')
            name = loc.get('result_object', {}).get('name')
            print(loc_id, city)
            existing_loc = CityLocation.query.filter_by(loc_id=loc_id).first()

            if not existing_loc and not loc_flag:
                loc_flag = True
                CreateLocationID(city=city, loc_id=loc_id, loc_flag=loc_flag)
                print(f"New Location committed to DB --> ID: {loc_id} City: {city}")
        else:
            print(f"Location already exists")
            break
    print(f"City: {city} completed")

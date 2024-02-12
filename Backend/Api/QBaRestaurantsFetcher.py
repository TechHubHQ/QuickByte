import requests
from app import app
from Backend.Models.QBmLoadRestaurantsByID import CreateRestaurant, RestaurantsByLoc
from Backend.Models.QBmLoadLocationID import CityLocation
from Backend.Connections.QBcDBConnector import db

app.app_context().push()
db.create_all()

url = "https://travel-advisor.p.rapidapi.com/restaurants/list"

headers = {
    "X-RapidAPI-Key": "897b3eccc5msh07c09ba21aae956p1040b7jsnbdaeb583f509",
    "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}

city_ids = CityLocation.query.with_entities(CityLocation.loc_id).distinct().all()
loc_ids = [city_id[0] for city_id in city_ids]

for loc_id in loc_ids:
    querystring = {"location_id": loc_id}
    response = requests.get(url, headers=headers, params=querystring)
    tmpResArr = response.json().get('data', [])

    for res in tmpResArr:
        res_flag = RestaurantsByLoc.query.filter_by(res_flag=None).first()
        if not res_flag:
            if None in (
                    res.get('location_id'), res.get('name'), res.get('num_reviews'), res.get('timezone'),
                    res.get('rating'),
                    res.get('ranking'), res.get('web_url'), res.get('phone'), res.get('email')):
                continue  # Skip this restaurant if any required field is None
            print("\nNew Restaurant -- registration")
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

            # Now you can insert this data into the database
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

import requests
# from Backend.app import app
# from Backend.Connections.QBcDBConnector import db

url = "https://foodiefetch.p.rapidapi.com/swiggy"

querystring = {"query": "Mazzo Hyderabad"}

headers = {
    "X-RapidAPI-Key": "897b3eccc5msh07c09ba21aae956p1040b7jsnbdaeb583f509",
    "X-RapidAPI-Host": "foodiefetch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

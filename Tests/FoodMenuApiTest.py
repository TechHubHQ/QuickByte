import requests

url = "https://foodiefetch.p.rapidapi.com/swiggy"

querystring = {"query": "Mazzo Hyderabad"}

# app_id = '0ff198fd'
# app_api_key = 'dadc61d87d86509431bd1f70937b5c0c'

headers = {
	"X-RapidAPI-Key": "897b3eccc5msh07c09ba21aae956p1040b7jsnbdaeb583f509",
	"X-RapidAPI-Host": "foodiefetch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

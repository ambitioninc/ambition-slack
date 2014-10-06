import requests


def lat_long_lookup(location):
    variables = {'address': location, 'sensor': 'false'}
    payload = requests.get("https://maps.googleapis.com/maps/api/geocode/json",
                           params=variables)
    payload = payload.json()
    latitude = payload["results"][0]["geometry"]["location"]["lat"]
    longitude = payload["results"][0]["geometry"]["location"]["lng"]
    return latitude, longitude

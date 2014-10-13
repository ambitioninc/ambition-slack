import requests


def lat_long_lookup(location):
    """takes in the location/zip from /weather and outputs the latitude and longitude in a tuple"""
    variables = {'address': location, 'sensor': 'false'}
    payload = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=variables)
    payload = payload.json()
    latitude = payload['results'][0]['geometry']['location']['lat']
    longitude = payload['results'][0]['geometry']['location']['lng']
    return latitude, longitude

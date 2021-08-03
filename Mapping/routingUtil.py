import requests
import re

mapbox_token = "pk.eyJ1IjoiYm9uYWxsdXJlIiwiYSI6ImNrbDBkMjdmNjA3MGIyb29laXEwZ2hqejIifQ.QaqbnympPVBZcyYbPlrlYQ"


def get_geolocation(address):
    # proper address format: 123 Main St Boston MA 02111

    base_address = re.sub(", ", '%20', address)
    address_param = re.sub(" ", '%20', base_address)

    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/%s.json?" % address_param
    params = {"country": "US", "access_token": mapbox_token}
    request = requests.get(url=url, params=params)
    response = request.json()
    # do some kind of response validation

    longitude = response['features'][0]['center'][0]
    latitude = response['features'][0]['center'][1]
    formatted_address = response['features'][0]['place_name']
    # reverse geolocation will be used to verify that the formatted and original address match.
    # print(formatted_address)

    return longitude, latitude


def get_address(address):
    # proper address format: 123 Main St Boston MA 02111

    base_address = re.sub(", ", '%20', address)
    address_param = re.sub(" ", '%20', base_address)

    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/%s.json?" % address_param
    params = {"country": "US", "access_token": mapbox_token}
    request = requests.get(url=url, params=params)
    response = request.json()
    # do some kind of response validation

    longitude = response['features'][0]['center'][0]
    latitude = response['features'][0]['center'][1]
    formatted_address = response['features'][0]['place_name']
    # reverse geolocation will be used to verify that the formatted and original address match.
    return formatted_address


def get_route(origin, destination):
    url = "https://api.mapbox.com/directions/v5/mapbox/driving/%s,%s;%s,%s?" % (
        origin[0], origin[1], destination[0], destination[1])
    params = {"steps": "true", "access_token": mapbox_token}
    request = requests.get(url=url, params=params)
    response = request.json()

    return response

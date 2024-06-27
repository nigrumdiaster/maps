import requests

def get_location_from_address(location_address, bing_maps_key):
    # Construct the request URL
    url = 'http://dev.virtualearth.net/REST/v1/Locations'
    params = {
        'query': location_address,
        'key': bing_maps_key
    }

    # Make the request to Bing Maps API
    response = requests.get(url, params=params)
    data = response.json()

    # Parse the response to get the latitude and longitude
    if data['resourceSets'] and data['resourceSets'][0]['resources']:
        location = data['resourceSets'][0]['resources'][0]['point']['coordinates']
        location_latitude = location[0]
        location_longitude = location[1]
    else:
        location_latitude = None
        location_longitude = None

    return location_latitude, location_longitude
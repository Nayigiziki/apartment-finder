import requests
import json
import googlemaps
from datetime import datetime
import config

gmaps = googlemaps.Client(key=config.MAPS_KEY)

try:
    from private import *
except Exception:
    pass

def drivingTimeToOffice(startLat, startLong, officeAddress):
    now = datetime.now()
    directions_result = gmaps.directions(origin=(startLat, startLong),
                                     destination=officeAddress,
                                     mode="driving",
                                     departure_time=now)

    return directions_result[0]['legs'][0]['duration']['text']

def geoCodeAddress(lat, long):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%f,%f&key=%s'%(lat, long, config.MAPS_KEY)
    r = requests.get(url)
    json = r.json()

    return json['results'][0]['formatted_address']

def walkingTimeFromTo(fromLat, fromLong, toLat, toLong):
    now = datetime.now()
    directions_result = gmaps.directions(origin=(fromLat, fromLong),
                                     destination=(toLat, toLong),
                                     mode="walking",
                                     departure_time=now)
    
    return directions_result[0]['legs'][0]['duration']['text']




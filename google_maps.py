import requests
import json

try:
    from private import *
except Exception:
    pass


def drivingTimeToOffice(startLat, startLong, officeAddress):
    url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%f,%f&destination=%s&sensor=false&alternatives=false&departure_time=1493827772&mode=driving?key=%s'%(startLat, startLong, officeAddress, GOOGLE_DIRECTION_API_KEY)
    r = requests.get(url)
    json = r.json()
    return json['routes'][0]['legs'][0]['duration']['text']

def geoCodeAddress(lat, long):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%f,%f&key=%s'%(lat, long, GOOGLE_GEOCODE_API_KEY)
    r = requests.get(url)
    json = r.json()
    return json['results'][0]['formatted_address']

def walkingTimeFromTo(fromLat, fromLong, toLat, toLong):
    url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%f,%f&destination=%f,%f&sensor=false&alternatives=false&departure_time=1493827772&mode=walking?key=%s'%(fromLat, fromLong, toLat, toLong, GOOGLE_DIRECTION_API_KEY)
    r = requests.get(url)
    json = r.json()
    return json['routes'][0]['legs'][0]['duration']['text']

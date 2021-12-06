import googlemaps
import pandas as pd
from fastapi import APIRouter, HTTPException, status, Body, Depends
from utils.ai import translate
from utils.maps import miles_to_meters


API_KEY = 'AIzaSyAOrGBEx8oXmC5rtzjps5028heX-Gk7EcI'
client = googlemaps.Client(API_KEY)

router = APIRouter()


@router.get('/nearbyplaces')
async def map_nearbyplaces(lat, lon):
    location = (lat, lon)
    distance = miles_to_meters(15)
    places = []
    response = client.places_nearby(
        location=location, keyword='', radius=distance)
    places.extend(response.get('results'))
    return list(map((lambda x: {
        "name": x.get('name', ''),
        "id": x.get("place_id", ''),
        "types": list(map(lambda x: translate(x), x.get("types", []))),
        "location": x.get("vicinity", ''),
        "rating": x.get("rating", ''),
        "opening_hours": x.get("opening_hours", ''),
    }), places))

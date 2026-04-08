import requests
from typing import List

GEOCODING_REQUEST_URL = "https://geocoding-api.open-meteo.com/v1/search?name={city_name}&language=he&format=json"
GEO_FIELDS = ["latitude", "longitude"]


def get_city_coordinates(city: str) -> dict:
    """Returns the coordinates for hebrew city names"""
    request_url = GEOCODING_REQUEST_URL.format(city_name=city)
    response = requests.get(request_url, timeout=15)
    if not response.ok:
        return {"status": "error", "message": response.text}
    if not "results" in response.json():
        raise ValueError("City name not found!")
    geo_data = response.json()["results"][0]
    geo_data = {k: v for k, v in geo_data.items() if k in GEO_FIELDS}
    print("GEODATA", geo_data)
    return geo_data


def filter_dict(d: dict, fields: List[str]):
    filtered_d = {k: v for k, v in d.items() if k in fields}
    return filtered_d

import requests
from typing import Optional, Literal


GEOCODING_REQUEST_URL = "https://geocoding-api.open-meteo.com/v1/search?name={city_name}&language=he&format=json"
AIRQUALITY_REQUEST_URL = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&current=european_aqi&hourly=european_aqi&forecast_days=2"

GEO_FIELDS = ["latitude", "longitude"]
AIRQ_FIELDS = ["tempC", "chanceofrain", "humidity", "weatherDesc", "uvIndex"]


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


def get_air_quality(
    city: str, day: Optional[Literal["today", "tomorrow"]] = None
) -> dict:
    """Get air quality data for a city

    Returns the current air quality and a forecast for the next 2 days

    Args:
        city: name of the city (in hebrew) ("תל אביב", "מודיעין", "פריז", etc).
        day: "today" or "tomorrow", optional. no mention will return both - good for comparison.
    Returns:
        A list of dicts representing temperature and humidity levels in the specified city at the specified times.
    """
    try:
        city_coordinates = get_city_coordinates(city=city)
    except ValueError as e:
        return {"status": "error", "message": e}
    request_url = AIRQUALITY_REQUEST_URL.format(**city_coordinates)

    response = requests.get(request_url, timeout=15)
    if response.status_code != 200:
        return {
            "status": "error",
            "message": response.text,
        }
    airq_data = response.json()
    current_airq = airq_data["current"]["european_aqi"]
    forecast_airq = airq_data["hourly"]
    forecast_airq = {
        k: v for k, v in zip(forecast_airq["time"], forecast_airq["european_aqi"])
    }

    airq_result = {"current": current_airq, "forecast": forecast_airq}

    return airq_result

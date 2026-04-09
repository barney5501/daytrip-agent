import requests
from typing import Optional, Literal
from .utils import get_city_coordinates, filter_dict

AIRQUALITY_REQUEST_URL = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&current=european_aqi&hourly=european_aqi&forecast_days=2"


def get_air_quality(
    city: str, day: Optional[Literal["today", "tomorrow"]] = None
) -> dict:
    """Get air quality data for a city

    Returns the current air quality and a forecast for the next 2 days

    Args:
        city: name of the city (in hebrew) ("תל אביב", "מודיעין", "פריז", etc).
        day: "today" or "tomorrow", optional. no mention will return both - good for comparison.
    Returns:
        a dictionary with the current air quality (under "current") and the air quality for every hour in the next 2 days (under "forecast").
        notes:  - the air quality is represented in EAQI (european aqi).
                - the timestamps are in the GMT timezone and you may have to convert them for accuracy.
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
    forecast_airq_times = forecast_airq["time"]
    forecast_airq_values = forecast_airq["european_aqi"]
    if day:
        forecast_airq_times = (
            forecast_airq_times[:24] if day == "today" else forecast_airq_times[24:]
        )
        forecast_airq_values = (
            forecast_airq_values[:24] if day == "today" else forecast_airq_values[24:]
        )
    forecast_airq = {k: v for k, v in zip(forecast_airq_times, forecast_airq_values)}
    airq_result = {"current": current_airq, "forecast": forecast_airq}

    return airq_result

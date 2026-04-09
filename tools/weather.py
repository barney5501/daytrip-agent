import requests
from typing import Optional, Literal, List
from .utils import get_city_coordinates, filter_dict
from dotenv import load_dotenv
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

WEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/forecast?units=metric&lat={latitude}&lon={longitude}&appid={api_key}"
WEATHER_FIELDS = ["temp", "humidity", "description"]


def get_time_range(start_time: int, end_time: Optional[int] = None) -> List[int]:
    """Returns a list of hour indices (in 3 hours intervals) from a range of hours"""
    start_time_index = start_time // 3
    end_time_index = end_time // 3 if end_time is not None else start_time_index
    return list(range(start_time_index, end_time_index + 1))


def get_weather_conditions(
    city: str,
    day: Literal["today", "tomorrow", "day_after_tomorrow"],
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
) -> List[dict]:
    """Get weather data for a city

    Returns hourly weather conditions (temp, humidity, etc) for a city.

    Args:
        city: name of the city ("תל אביב", "מודיעין", "פריז", etc).
        day: "today", "tomorrow", or "day_after_tomorrow".
        start_time: Optional. 0-23. hour of the day. if not provided will return data the entire day.
        end_time: Optional. 0-23. hour of the day, if provided the response will be from the start_time to the end_time
    Returns:
        A list of dicts representing temperature and humidity levels in the specified city at the specified times.
    """

    city_coordinates = get_city_coordinates(city=city)
    request_url = WEATHER_REQUEST_URL.format(
        **city_coordinates, api_key=WEATHER_API_KEY
    )

    response = requests.get(request_url, timeout=15)
    if response.status_code != 200:
        return [
            {
                "status": "error",
                "message": response.text,
            }
        ]
    weather_data = response.json()["list"]
    weather_data = [
        filter_dict(d=day, fields=["main", "weather"]) for day in weather_data
    ]
    weather_data = [
        filter_dict(d=day["main"], fields=WEATHER_FIELDS)
        | filter_dict(d=day["weather"][0], fields=WEATHER_FIELDS)
        for day in weather_data
    ]

    if day == "today":
        weather_data = weather_data[:8]
    elif day == "tomorrow":
        weather_data = weather_data[8:16]
    else:
        weather_data = weather_data[16:24]

    if start_time is not None:
        time_range = get_time_range(start_time=start_time, end_time=end_time)
        weather_data = weather_data[time_range[0] : time_range[-1] + 1]

    return weather_data

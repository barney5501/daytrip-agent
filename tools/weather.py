import requests
from typing import Optional, Literal, List
from utils import filter_dict

WEATHER_REQUEST_URL = "https://wttr.in/{city}?format=j1"
DAY_LITERAL_MAP = {"today": 0, "tomorrow": 1, "day_after_tomorrow": 2}
WEATHER_FIELDS = ["tempC", "chanceofrain", "humidity", "weatherDesc", "uvIndex"]


def get_time_range(start_time: int, end_time: Optional[int] = None) -> List[int]:
    """Returns a list of hour indices (in 3 hours intervals) from a range of hours"""
    start_time_index = start_time // 3
    end_time_index = end_time // 3 if end_time is not None else start_time_index
    return list(range(start_time_index, end_time_index + 1))


def get_weather_conditions(
    city: str,
    day: Literal["today", "tomorrow", "day_after_tomorrow"],
    start_time: Optional[int] = 0,
    end_time: Optional[int] = 23,
) -> List[dict]:
    """Get weather data for a city

    Returns hourly weather conditions (temp, humidity, etc) for a city.

    Args:
        city: name of the city in english ("tel-aviv", "modiin", "paris", etc).
        day: "today", "tomorrow", or "day_after_tomorrow".
        start_time: Optional. 0-23. hour of the day. if not provided will return data the entire day.
        end_time: Optional. 0-23. hour of the day, if provided the response will be from the start_time to the end_time
    Returns:
        A list of dicts representing temperature and humidity levels in the specified city at the specified times.
    """

    request_url = WEATHER_REQUEST_URL.format(city=city)

    response = requests.get(request_url, timeout=15)
    if response.status_code != 200:
        return [
            {
                "status": "error",
                "message": response.text,
            }
        ]
    weather_data = response.json()
    weather_data = weather_data["weather"][DAY_LITERAL_MAP[day]]["hourly"]
    weather_data = [
        filter_dict(d=section, fields=WEATHER_FIELDS) for section in weather_data
    ]

    if start_time is not None:
        time_range = get_time_range(start_time=start_time, end_time=end_time)
        weather_data = weather_data[time_range[0] : time_range[-1] + 1]

    return weather_data

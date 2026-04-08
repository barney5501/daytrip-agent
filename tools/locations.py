import requests
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
api_key = os.getenv("LOCATIONIQ_API_KEY")

PLACES_REQUEST_URL = locationiq_url = (
    "https://us1.locationiq.com/v1/search?key={api_key}&q={query_string}&format=json"
)
PLACES_FIELDS = ["display_name", "lat", "lon"]


def get_places_location(location_query: str) -> List[dict]:
    """Get location data for places from a query

    Returns the lat and lon of a location in based on a query for the name of the place (example: "ארומה ישפרו מודיעין")

    Args:
        location_query: query string for a place (restaurant/cafe, viewpoint, shop)
    Returns:
        A list of dicts (name, lat, lon) for each location found relevant to the query
    """

    request_url = PLACES_REQUEST_URL.format(
        api_key=api_key, query_string=location_query
    )

    response = requests.get(request_url, timeout=15)
    if not response.ok:
        return [
            {
                "status": "error",
                "message": response.text,
            }
        ]
    location_data = response.json()
    location_data = [
        {k: v for k, v in location.items() if k in PLACES_FIELDS}
        for location in location_data
    ]

    return location_data

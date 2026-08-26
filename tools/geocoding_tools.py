import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")


def get_coordinates(location: str):
    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": location,
        "apiKey": GEOAPIFY_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        features = data.get("features", [])

        if not features:
            return None

        properties = features[0]["properties"]

        return {
            "location": properties.get("formatted"),
            "latitude": properties.get("lat"),
            "longitude": properties.get("lon"),
            "country": properties.get("country")
        }

    except requests.exceptions.RequestException as e:
        print("Geocoding error:", e)
        return None
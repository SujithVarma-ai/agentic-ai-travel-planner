
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

GEOCODING_URL = "https://api.geoapify.com/v1/geocode/search"


def get_coordinates(location: str):
    """
    Find a location dynamically using Geoapify.

    Defaults to India because this travel planner focuses
    on Indian destinations. No fixed city list is required.
    """

    if not GEOAPIFY_API_KEY:
        print("Geocoding error: GEOAPIFY_API_KEY is missing.")
        return None

    if not location or not location.strip():
        return None

    params = {
        "text": location.strip(),
        "filter": "countrycode:in",
        "limit": 5,
        "lang": "en",
        "apiKey": GEOAPIFY_API_KEY,
    }

    try:
        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=15,
        )
        response.raise_for_status()

        data = response.json()
        features = data.get("features", [])

        if not features:
            print(f"Location not found in India: {location}")
            return None

        # Prefer an Indian result if the API returns one.
        properties = next(
            (
                feature.get("properties", {})
                for feature in features
                if feature.get("properties", {}).get(
                    "country_code"
                ) == "in"
            ),
            features[0].get("properties", {}),
        )

        latitude = properties.get("lat")
        longitude = properties.get("lon")

        if latitude is None or longitude is None:
            print(f"Coordinates unavailable for: {location}")
            return None

        return {
            "location": properties.get("formatted") or location.strip(),
            "latitude": latitude,
            "longitude": longitude,
            "country": properties.get("country"),
            "state": properties.get("state"),
            "city": (
                properties.get("city")
                or properties.get("town")
                or properties.get("village")
                or properties.get("municipality")
            ),
            "country_code": properties.get("country_code"),
        }

    except requests.exceptions.RequestException as error:
        print(f"Geocoding error: {error}")
        return None

    except (ValueError, KeyError) as error:
        print(f"Could not process geocoding response: {error}")
        return None

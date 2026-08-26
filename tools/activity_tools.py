import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")


def get_activities(latitude, longitude, limit=10):
    url = "https://opentripmap-places-v1.p.rapidapi.com/en/places/radius"

    params = {
        "radius": 10000,
        "lon": longitude,
        "lat": latitude,
        "limit": limit,
        "rate": 2,
        "format": "json"
    }

    headers = {
        "X-RapidAPI-Key": OPENTRIPMAP_API_KEY,
        "X-RapidAPI-Host": "opentripmap-places-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        data = response.json()

        activities = []

        for place in data:
            name = place.get("name")

            if name:
                activities.append({
                    "name": name,
                    "kind": place.get("kinds"),
                    "latitude": place.get("point", {}).get("lat"),
                    "longitude": place.get("point", {}).get("lon")
                })

        return activities

    except requests.exceptions.RequestException as e:
        print("Activity error:", e)
        return None
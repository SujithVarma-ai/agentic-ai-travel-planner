
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

OPENTRIPMAP_URL = (
    "https://opentripmap-places-v1.p.rapidapi.com/"
    "en/places/radius"
)


def get_activities(latitude, longitude, limit=20, radius=20000):
    """
    Find nearby attractions using OpenTripMap.

    Args:
        latitude: Destination latitude.
        longitude: Destination longitude.
        limit: Maximum number of results requested.
        radius: Search radius in meters (default 20 km).

    Returns:
        A list of attractions. Returns an empty list if
        no results are available or the request fails.
    """

    if not OPENTRIPMAP_API_KEY:
        print("Activity error: OPENTRIPMAP_API_KEY is missing.")
        return []

    try:
        latitude = float(latitude)
        longitude = float(longitude)

        if not (-90 <= latitude <= 90):
            print("Activity error: Invalid latitude.")
            return []

        if not (-180 <= longitude <= 180):
            print("Activity error: Invalid longitude.")
            return []

        # Keep requests within reasonable limits.
        limit = max(1, min(int(limit), 50))
        radius = max(1000, min(int(radius), 50000))

        params = {
            "radius": radius,
            "lon": longitude,
            "lat": latitude,
            "limit": limit,
            "rate": 1,
            "format": "json",
        }

        headers = {
            "X-RapidAPI-Key": OPENTRIPMAP_API_KEY,
            "X-RapidAPI-Host": (
                "opentripmap-places-v1.p.rapidapi.com"
            ),
        }

        response = requests.get(
            OPENTRIPMAP_URL,
            headers=headers,
            params=params,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            print("Activity error: Unexpected API response.")
            return []

        activities = []
        seen = set()

        for place in data:
            name = (place.get("name") or "").strip()

            if not name:
                continue

            point = place.get("point") or {}
            lat = point.get("lat")
            lon = point.get("lon")

            # Prefer the API's unique ID to remove duplicates.
            place_id = place.get("xid")

            if place_id:
                unique_key = place_id
            else:
                unique_key = (
                    name.casefold(),
                    lat,
                    lon,
                )

            if unique_key in seen:
                continue

            seen.add(unique_key)

            activities.append({
                "name": name,
                "kind": place.get("kinds") or "",
                "latitude": lat,
                "longitude": lon,
                "distance": place.get("dist"),
                "xid": place_id,
            })

        # Put closer attractions first when distance is available.
        activities.sort(
            key=lambda item: (
                item["distance"]
                if isinstance(item["distance"], (int, float))
                else float("inf")
            )
        )

        return activities

    except (ValueError, TypeError) as error:
        print(f"Activity error: Invalid input: {error}")
        return []

    except requests.exceptions.RequestException as error:
        print(f"Activity API error: {error}")
        return []

    except (KeyError, AttributeError, ValueError) as error:
        print(f"Activity response error: {error}")
        return []

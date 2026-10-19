
import time
import requests

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude, longitude, retries=3):
    """
    Fetch current weather from Open-Meteo.
    Returns a dictionary or None if the service is unavailable.
    """
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None

    if not (-90 <= latitude <= 90):
        return None

    if not (-180 <= longitude <= 180):
        return None

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    for attempt in range(retries):
        try:
            response = requests.get(
                WEATHER_URL,
                params=params,
                timeout=15,
            )

            if response.status_code in (429, 500, 502, 503, 504):
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue

                print(
                    "Weather service temporarily unavailable:",
                    response.status_code,
                )
                return None

            response.raise_for_status()
            data = response.json()
            current = data.get("current")

            if not current:
                print("Weather response did not contain current conditions.")
                return None

            return {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "weather_code": current.get("weather_code"),
                "wind_speed": current.get("wind_speed_10m"),
                "timezone": data.get("timezone"),
                "data_type": "live",
            }

        except (requests.exceptions.RequestException, ValueError) as error:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue

            print(f"Weather request failed: {error}")
            return None

    return None

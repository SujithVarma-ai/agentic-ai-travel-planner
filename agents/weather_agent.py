from tools.geocoding_tools import get_coordinates
from tools.weather_tools import get_weather


class WeatherAgent:

    def run(self, destination):

        location = get_coordinates(destination)

        if not location:
            return {
                "weather": None,
                "error": "Could not find the destination."
            }

        weather = get_weather(
            latitude=location["latitude"],
            longitude=location["longitude"]
        )

        return {
            "destination": location["location"],
            "weather": weather
        }
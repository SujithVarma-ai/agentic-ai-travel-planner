from tools.geocoding_tools import get_coordinates
from tools.weather_tools import get_weather

location = get_coordinates("Goa, India")

if location:
    weather = get_weather(
        location["latitude"],
        location["longitude"]
    )

    print(weather)
from tools.geocoding_tools import get_coordinates
from tools.activity_tools import get_activities


location = get_coordinates("Goa, India")

if location:
    activities = get_activities(
        location["latitude"],
        location["longitude"]
    )

    print(activities)
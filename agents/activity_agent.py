
from tools.geocoding_tools import get_coordinates
from tools.activity_tools import get_activities


class ActivityAgent:
    def run(self, destination):
        location = get_coordinates(destination)

        if not location:
            return {
                "destination": destination,
                "activities": [],
                "error": "Could not find the destination.",
            }

        activities = get_activities(
            latitude=location["latitude"],
            longitude=location["longitude"],
        )

        # Never allow a failed API response (None) to propagate.
        if not isinstance(activities, list):
            activities = []

        return {
            "destination": location["location"],
            "activities": activities,
        }

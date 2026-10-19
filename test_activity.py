
from tools.geocoding_tools import get_coordinates
from tools.activity_tools import get_activities

destinations = [
    "Darjeeling, West Bengal",
    "Pelling, Sikkim",
    "Gangtok, Sikkim",
    "Kedarnath, Uttarakhand",
    "Badrinath, Uttarakhand",
    "Ziro, Arunachal Pradesh",
    "Majuli, Assam",
]

for destination in destinations:
    print(f"\n{'=' * 50}")
    print(f"Destination: {destination}")

    location = get_coordinates(destination)

    if not location:
        print("Destination could not be resolved.")
        continue

    activities = get_activities(
        latitude=location["latitude"],
        longitude=location["longitude"],
        limit=20,
        radius=20000,
    )

    print(f"Attractions found: {len(activities)}")

    for index, activity in enumerate(activities, start=1):
        print(f"{index}. {activity['name']} ({activity['kind']})")

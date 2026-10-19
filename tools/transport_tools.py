import random
from tools.geocoding_tools import get_coordinates

AIRLINES = ["IndiGo", "Air India", "Akasa Air"]


def search_flights(origin, destination):
    # Resolve both cities using Geoapify.
    origin_location = get_coordinates(origin)
    destination_location = get_coordinates(destination)

    if not origin_location:
        return {
            "error": f"Could not find origin: {origin}"
        }

    if not destination_location:
        return {
            "error": f"Could not find destination: {destination}"
        }

    origin_city = origin_location["location"]
    destination_city = destination_location["location"]

    # Prevent trips between the same coordinates.
    if (
        origin_location["latitude"]
        == destination_location["latitude"]
        and origin_location["longitude"]
        == destination_location["longitude"]
    ):
        return {
            "error": "Origin and destination cannot be the same."
        }

    # Generate consistent simulated fares for each route.
    rng = random.Random(
        f"{origin_city}|{destination_city}"
    )

    base_price = rng.randint(3000, 9000)
    flights = []

    for i, airline in enumerate(AIRLINES):
        duration_minutes = rng.randint(60, 240)
        price = max(
            1000,
            base_price + rng.randint(-500, 1500)
        )

        flights.append({
            "origin": origin_city,
            "destination": destination_city,
            "airline": airline,
            "price": price,
            "currency": "INR",
            "duration": (
                f"{duration_minutes // 60}h "
                f"{duration_minutes % 60}m"
            ),
            "stops": 0 if i < 2 else 1,
            "data_type": "simulated"
        })

    return flights
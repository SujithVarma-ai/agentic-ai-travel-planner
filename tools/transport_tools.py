import random


# Major Indian cities supported by the project
INDIAN_CITIES = {
    "hyderabad": "Hyderabad",
    "mumbai": "Mumbai",
    "delhi": "Delhi",
    "new delhi": "Delhi",
    "bengaluru": "Bengaluru",
    "bangalore": "Bengaluru",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "goa": "Goa",
    "pune": "Pune",
    "jaipur": "Jaipur",
    "ahmedabad": "Ahmedabad",
    "kochi": "Kochi",
    "cochin": "Kochi",
    "thiruvananthapuram": "Thiruvananthapuram",
    "trivandrum": "Thiruvananthapuram",
    "visakhapatnam": "Visakhapatnam",
    "vizag": "Visakhapatnam",
    "lucknow": "Lucknow",
    "varanasi": "Varanasi",
    "indore": "Indore",
    "bhubaneswar": "Bhubaneswar",
    "chandigarh": "Chandigarh",
    "amritsar": "Amritsar",
    "coimbatore": "Coimbatore",
    "nagpur": "Nagpur"
}


AIRLINES = [
    "IndiGo",
    "Air India",
    "Akasa Air",
    "SpiceJet"
]


def normalize_city(city):
    city = city.lower().strip()

    # Remove ", India" if present
    city = city.replace(", india", "").strip()

    return INDIAN_CITIES.get(city)


def search_flights(origin, destination):
    """
    Returns simulated flight options for supported
    Indian domestic routes.
    """

    origin_city = normalize_city(origin)
    destination_city = normalize_city(destination)

    # Check whether cities are supported
    if not origin_city:
        return {
            "error": f"Origin '{origin}' is not currently supported."
        }

    if not destination_city:
        return {
            "error": f"Destination '{destination}' is not currently supported."
        }

    # Same origin and destination
    if origin_city == destination_city:
        return {
            "error": "Origin and destination cannot be the same."
        }

    # Generate a consistent seed for the route
    random.seed(origin_city + destination_city)

    base_price = random.randint(3000, 9000)
    duration_minutes = random.randint(60, 180)

    flights = []

    for i in range(3):

        price = base_price + random.randint(-500, 1500)

        hours = duration_minutes // 60
        minutes = duration_minutes % 60

        flights.append({
            "origin": origin_city,
            "destination": destination_city,
            "airline": AIRLINES[i],
            "price": price,
            "currency": "INR",
            "duration": f"{hours}h {minutes}m",
            "stops": 0 if i < 2 else 1,
            "data_type": "simulated"
        })

    return flights
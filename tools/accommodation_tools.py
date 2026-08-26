import random


def search_hotels(destination):
    destination = destination.strip().title()

    random.seed(destination)

    hotel_names = [
        "Grand Residency",
        "Royal Stay",
        "Comfort Inn",
        "City View Hotel",
        "Travel Nest"
    ]

    hotels = []

    for i in range(3):
        price = random.randint(1500, 8000)

        hotels.append({
            "name": f"{hotel_names[i]} {destination}",
            "location": destination,
            "price_per_night": price,
            "currency": "INR",
            "rating": round(random.uniform(3.5, 5.0), 1),
            "data_type": "simulated"
        })

    return hotels
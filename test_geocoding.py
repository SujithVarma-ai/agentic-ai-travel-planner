
from tools.geocoding_tools import get_coordinates

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
    print(f"\nSearching: {destination}")
    result = get_coordinates(destination)
    print(result)

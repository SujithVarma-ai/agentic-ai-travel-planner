from tools.accommodation_tools import search_hotels


class AccommodationAgent:

    def run(self, destination):

        hotels = search_hotels(destination)

        return {
            "accommodation": hotels
        }
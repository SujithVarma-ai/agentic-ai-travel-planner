from tools.transport_tools import search_flights


class TransportAgent:

    def run(self, origin, destination):

        flights = search_flights(
            origin=origin,
            destination=destination
        )

        return {
            "transport": flights
        }
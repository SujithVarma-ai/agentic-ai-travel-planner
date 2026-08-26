class BudgetAgent:

    def run(self, flights, hotels, days):
        
        # Select the cheapest flight
        cheapest_flight = min(
            flights,
            key=lambda flight: flight["price"]
        )

        # Select the cheapest hotel
        cheapest_hotel = min(
            hotels,
            key=lambda hotel: hotel["price_per_night"]
        )

        flight_cost = cheapest_flight["price"]

        hotel_cost = (
            cheapest_hotel["price_per_night"] * days
        )

        # Estimated food and local expenses per day
        daily_other_expenses = 1500

        other_cost = daily_other_expenses * days

        total_cost = (
            flight_cost +
            hotel_cost +
            other_cost
        )

        return {
            "selected_flight": cheapest_flight,
            "selected_hotel": cheapest_hotel,
            "flight_cost": flight_cost,
            "hotel_cost": hotel_cost,
            "other_expenses": other_cost,
            "total_estimated_cost": total_cost,
            "currency": "INR"
        }
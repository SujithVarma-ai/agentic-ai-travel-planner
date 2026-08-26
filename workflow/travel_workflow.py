from agents.transport_agent import TransportAgent
from agents.accommodation_agent import AccommodationAgent
from agents.activity_agent import ActivityAgent
from agents.weather_agent import WeatherAgent
from agents.budget_agent import BudgetAgent
from agents.recommendation_agent import RecommendationAgent


class TravelWorkflow:

    def __init__(self):

        self.transport_agent = TransportAgent()
        self.accommodation_agent = AccommodationAgent()
        self.activity_agent = ActivityAgent()
        self.weather_agent = WeatherAgent()
        self.budget_agent = BudgetAgent()
        self.recommendation_agent = RecommendationAgent()


    def run(self, origin, destination, days):

        # 1. Get flight options
        transport_result = self.transport_agent.run(
            origin,
            destination
        )

        # 2. Get hotel options
        accommodation_result = self.accommodation_agent.run(
            destination
        )

        # 3. Get activities
        activity_result = self.activity_agent.run(
            destination
        )

        # 4. Get weather
        weather_result = self.weather_agent.run(
            destination
        )

        # 5. Calculate budget
        budget_result = self.budget_agent.run(
            flights=transport_result["transport"],
            hotels=accommodation_result["accommodation"],
            days=days
        )

        # 6. Generate AI recommendation
        recommendation = self.recommendation_agent.run(
            destination=destination,
            days=days,
            weather=weather_result["weather"],
            activities=activity_result["activities"],
            budget=budget_result
        )

        # Final result
        return {
            "origin": origin,
            "destination": destination,
            "days": days,
            "transport": transport_result,
            "accommodation": accommodation_result,
            "activities": activity_result,
            "weather": weather_result,
            "budget": budget_result,
            "recommendation": recommendation
        }
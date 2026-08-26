from agents.activity_agent import ActivityAgent
from agents.weather_agent import WeatherAgent
from agents.recommendation_agent import RecommendationAgent


activity_agent = ActivityAgent()
weather_agent = WeatherAgent()
recommendation_agent = RecommendationAgent()


destination = "Goa, India"
days = 3

activity_result = activity_agent.run(destination)
weather_result = weather_agent.run(destination)

budget = {
    "total_estimated_cost": 27357,
    "currency": "INR"
}

result = recommendation_agent.run(
    destination=destination,
    days=days,
    weather=weather_result["weather"],
    activities=activity_result["activities"],
    budget=budget
)

print(result)
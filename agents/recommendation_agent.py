import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


class RecommendationAgent:

    def run(
        self,
        destination,
        days,
        weather,
        activities,
        budget
    ):

        prompt = f"""
You are an intelligent AI travel recommendation agent.

Create a personalized travel recommendation for the user.

Destination: {destination}
Number of days: {days}

Current Weather:
{weather}

Available Activities:
{activities}

Estimated Budget:
{budget}

Based on this information:

1. Recommend the best activities.
2. Consider the weather while recommending activities.
3. Create a simple day-by-day itinerary.
4. Mention the estimated total budget.
5. Give useful travel advice.

Keep the response clear, practical, and well structured.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text
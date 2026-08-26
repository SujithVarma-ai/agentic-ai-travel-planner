from models.travel_models import TravelRequest


class PlanningAgent:
    """
    Planning Agent responsible for understanding the user's
    travel request and creating a sequence of tasks.
    """

    def __init__(self):
        self.name = "Planning Agent"

    def create_plan(self, request: TravelRequest) -> list[str]:
        """
        Create a travel planning workflow based on the user's request.
        """

        plan = [
            "Find suitable transportation options",
            "Find suitable accommodation options",
            "Find activities matching the user's interests",
            "Calculate the estimated trip budget",
            "Check whether the trip fits within the user's budget",
            "Generate the final travel recommendation"
        ]

        return plan

    def display_plan(self, request: TravelRequest, plan: list[str]) -> None:
        """
        Display the planning agent's execution plan.
        """

        print(f"\n{'=' * 50}")
        print(f"{self.name}")
        print(f"{'=' * 50}")

        print("\nTravel Request:")
        print(f"Destination : {request.destination}")
        print(f"Duration    : {request.duration_days} days")
        print(f"Travelers   : {request.travelers}")
        print(f"Budget      : ₹{request.budget:,.2f}")
        print(f"Interests   : {', '.join(request.interests)}")

        if request.travel_dates:
            print(f"Travel Dates: {request.travel_dates}")

        print("\nExecution Plan:")

        for index, task in enumerate(plan, start=1):
            print(f"{index}. {task}")
from agents.transport_agent import TransportAgent
from agents.accommodation_agent import AccommodationAgent
from agents.budget_agent import BudgetAgent


transport_agent = TransportAgent()
accommodation_agent = AccommodationAgent()
budget_agent = BudgetAgent()


transport_result = transport_agent.run(
    "Hyderabad",
    "Goa"
)

accommodation_result = accommodation_agent.run(
    "Goa"
)


result = budget_agent.run(
    flights=transport_result["transport"],
    hotels=accommodation_result["accommodation"],
    days=3
)

print(result)
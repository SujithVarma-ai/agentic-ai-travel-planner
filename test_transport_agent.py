from agents.transport_agent import TransportAgent

agent = TransportAgent()

result = agent.run(
    origin="Hyderabad",
    destination="Goa"
)

print(result)
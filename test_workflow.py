from workflow.travel_workflow import TravelWorkflow


workflow = TravelWorkflow()

result = workflow.run(
    origin="Hyderabad",
    destination="Goa, India",
    days=3
)

print(result["recommendation"])
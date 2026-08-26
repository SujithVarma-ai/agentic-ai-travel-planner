from tools.transport_tools import search_flights

result = search_flights(
    origin="Hyderabad",
    destination="Goa"
)

print(result)
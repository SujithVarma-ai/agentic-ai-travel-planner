from tools.currency_tools import convert_currency

result = convert_currency(
    amount=50000,
    from_currency="INR",
    to_currency="USD"
)

print(result)
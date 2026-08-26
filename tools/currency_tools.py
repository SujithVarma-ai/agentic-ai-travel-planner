import requests


def convert_currency(amount, from_currency, to_currency):
    url = "https://api.frankfurter.app/latest"

    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        converted_amount = data["rates"][to_currency]

        return {
            "original_amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": converted_amount
        }

    except requests.exceptions.RequestException as e:
        print("Currency conversion error:", e)
        return None
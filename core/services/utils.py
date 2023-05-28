import requests


class Utils:

    @staticmethod
    def get_latest_exchange_rates(source_currency: str, target_currency: str, value: float) -> float:
        url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{source_currency}/{target_currency}.json"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            rate = data[target_currency]
            return value * rate
        else:
            raise Exception("Failed to fetch exchange rates.")

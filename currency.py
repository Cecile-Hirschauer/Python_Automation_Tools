import os
import requests 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

CURRENCIES = ["USD", "EUR", "CAD", "GBP", "INR"]

def currency_convert(base):
    currencies = ",".join(CURRENCIES)
    url = f"{BASE_URL}{API_KEY}&base_currency={base}&target_currency={currencies}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Vérification de la structure de la réponse
        if "data" not in data:
            print(f"Unexpected API response format: {data}")
            return None
        return data["data"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():
    while True:
        base = input("Enter the base currency (q to quit): ").upper()
        
        if base == "Q":
            print("Exiting...")
            exit()

        if base not in CURRENCIES:
            print("Invalid currency")
            exit()

        data = currency_convert(base)

        if data is None:
            print("An error occurred. Please try again.")
            continue

        if not data:
            print("No data found.")
            continue

        del data[base]
        for currency, value in data.items():
            print(f"{currency}: {value}")

if __name__ == "__main__":
    main()
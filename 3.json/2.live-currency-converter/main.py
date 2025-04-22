import json
import os
from dotenv import load_dotenv
from urllib.request import urlopen

load_dotenv()

api_key = os.getenv("CURRENCY_API_KEY")
url = f"https://api.currencyfreaks.com/latest?apikey={api_key}"
with urlopen(url) as response:
    raw_data = response.read()
    
data = json.loads(raw_data)
# print(json.dumps(data, indent=2))

base_currency = data["base"]
exchange_rates = data["rates"]

# for currency, rate in exchange_rates.items():
    # print(f"1 {base_currency} = {rate} {currency}")

print(f"\nCurrency Exchange Rate Tool (Base: {base_currency})\n")

while True:

    currency_code = input("Enter the currency code (or 'exit' to quit): ").strip().upper()

    if currency_code == "EXIT":
        print("Goodbye!")
        break

    if currency_code in exchange_rates:

        rate = float(exchange_rates[currency_code])
        print(f"1 {base_currency} = {rate} {currency_code}")

        try:
            amount = float(input(f"Enter amount in {base_currency}: "))
            amount_converted = amount * rate
            print(f"{amount} {base_currency} = {amount_converted:.2f} {currency_code}\n")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.\n")
    else:
        print("Currency not found. Please try again.\n")

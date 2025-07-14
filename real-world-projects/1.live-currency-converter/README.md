# Live Currency Converter (JSON + API)

This is a simple command-line currency converter built with Python using live exchange rates from the [CurrencyFreaks](https://currencyfreaks.com/) API.


### Features

- Fetches **live exchange rates** via JSON API
- Converts amount from base currency to any supported currency
- User-friendly CLI with input validation
- Demonstrates JSON parsing using built-in Python libraries


### 🛠️ Tools & Concepts Used

- Python Basics (variables, functions, loops, conditionals)

- Virtual Environment (`venv`) – to isolate project dependencies

- External API Integration – using `urllib.request` to fetch live currency rates

- Environment Variables – using `.env` files securely with `python-dotenv`

- JSON Handling – parsing API responses using the `json` module

- Error Handling – using `try/except` blocks to handle invalid user input

- User Interaction – using `input()` and while loops for a CLI-based tool

- Code Organization – keeping config like API keys separate from logic


### How to Run

1. Clone the repository and navigate to the project folder:

   `cd python-practice-projects/real-world-projects/1.live-currency-converter` 

2. Create and activate a virtual environment:

   `python3 -m venv .venv`
   `source .venv/bin/activate  # On Windows: .venv\Scripts\activate `

3. Install dependencies:

   `pip install -r requirements.txt`

4. From `env.example` file, copy the `.env` file and add your api key inside it:

   `cp .env.example .env`
   
   CURRENCY_API_KEY=your_api_key_here

5. Run the script:

   `python main.py`


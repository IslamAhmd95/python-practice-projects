import requests
import logging


def get_user_data(url):
    logging.info(f"Fetching data from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data")
    return response.json()
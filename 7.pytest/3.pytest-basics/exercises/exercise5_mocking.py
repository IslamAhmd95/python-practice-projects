import requests
import json
import time


def fetch_user(user_id: int):
    """Simulates an external API call."""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()


def write_to_file(filename: str, data: dict):
    """Writes JSON data to a file."""
    with open(filename, "w") as f:
        json.dump(data, f)
    return True


def get_timestamp():
    """Returns current UNIX timestamp."""
    return int(time.time())


class EmailService:
    """Pretend email service."""

    def send_email(self, to, subject, body):
        # Imagine this talks to AWS SES or Gmail API
        time.sleep(0.2)
        return {"status": "sent", "to": to}

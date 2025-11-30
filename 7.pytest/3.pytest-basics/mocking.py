import time

import requests


# Example 1: Mocking a Function

def get_price():
    print("Calling external API...")
    return 100

def total_price(qty):
    return get_price() * qty


# ----------------------------------------------------------

# Example 2: Mocking a Class

class EmailSender:
    def send(self, to, msg):
        print("Sending email...")
        return True


def notify(sender, user):
    return sender.send(user, "Welcome!")


# ----------------------------------------------------------

# Example 3: Mocking external HTTP requests


def fetch():
    r = requests.get("https://example.com")
    return r.status_code



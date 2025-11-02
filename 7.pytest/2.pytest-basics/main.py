import sys

def add(x, y):
    return x + y

def divide(numerator, denominator):
    if denominator == 0:
        raise ValueError("Can't divide by zero")
    return numerator / denominator


def report():
    # stdout same like "normal speaking voice"
    print("success")
    # stderr same like "angry warning voice"
    print("error", file=sys.stderr)
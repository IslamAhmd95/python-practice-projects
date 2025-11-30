import time

def fast_add(a, b):
    return a + b


def slow_multiply(a, b):
    """Artificially slow to test pytest markers."""
    time.sleep(0.3)
    return a * b


class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

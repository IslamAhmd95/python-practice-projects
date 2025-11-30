"""
1. Basic pytest structure
    - What is pytest?
    - Test file naming rules
    - Test function naming rules
    - Writing your first test
"""

def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def square(n):
    return n*n


def is_even(n):
    if n % 2 == 0:
        return True
    return False


def reverse_string(s):
    if len(s) == 0:
        raise ValueError("Please enter a valid string")
    return s[::-1]



if __name__ == "__main__":
    print(reverse_string("ISLAM"))
    print(reverse_string('i'))
    print(divide(5, 0))
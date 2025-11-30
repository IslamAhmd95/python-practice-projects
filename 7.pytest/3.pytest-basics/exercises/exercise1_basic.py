def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0

def reverse_string(s):
    if len(s) == 0:
        raise ValueError("Please enter a valid string")
    return s[::-1]

# return the max number from a list
def find_max(numbers):
    return max(numbers)


if __name__ == "__main__":
    print(reverse_string(""))

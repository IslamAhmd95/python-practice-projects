
__all__ = ["max_of_two", "filter_even", "get_age"] # you can define which functions are public to be imported outside


def max_of_two(a, b):
    if a == b:
        raise ValueError("a can't be equal to b")
    return max(a, b)


def filter_even(numbers):
    if len(numbers) == 0:
        raise ValueError("List can't be empty")
    return [n for n in numbers if n % 2 == 0]



def get_age(d):
    if "age" not in d:
        raise KeyError("Missing age")
    return d["age"]



if __name__ == "__main__":
    print(max_of_two(3, 4))
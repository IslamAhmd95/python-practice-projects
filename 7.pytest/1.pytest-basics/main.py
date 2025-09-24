def add(x, y):
    return x+y

def sub(x, y):
    return y - x

def divide(numerator, denominator):
    if denominator == 0:
        raise ValueError("Can't divide by zero")
    return numerator / denominator

def capitalize_each_word(statement):
    return statement.title()

def define_user(user):
    return f"Username is {user['name'].upper()}, user's age is {user['age']}"

# This comment "pragma: no cover" is a special comment, it tells coverage.py: “Don’t count these lines in the coverage report.”
if __name__ == '__main__':  # pragma: no cover
    print(capitalize_each_word("My name is islam"))  # pragma: no cover
    print(define_user({"name": "islam", "age": 30}))  # pragma: no cover
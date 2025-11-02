import main
import pytest   # pyright: ignore[reportMissingImports]



@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (-1, 5, 4),
    (0, 0, 0)
])
def test_add_various_cases(x, y, expected):
    assert main.add(x, y) == expected



@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 1),
    (5, 10, 5),
    (-3, 3, 6),
    (0, 0, 0),
])
def test_sub_various_cases(x, y, expected):
    assert expected == main.sub(x, y)



@pytest.mark.parametrize("x, y", [
    # we here are focusing on checking if the output is positive, we don't need to check if the sub operation itself is correct, it's already checked on the last test function, so no need for expected
    (1, 2),
    (5, 10),
    (-3, 3),
    (0, 0),
])
def test_sub_should_return_positive_result(x, y):
    result = main.sub(x, y)
    assert result >= 0




@pytest.mark.parametrize("numerator, denominator, expected", [
    (10, 5, 2),
    (8, 4, 2),
    (12, 3, 4),
    (0, 1, 0)
])
def test_divide_normal_cases(numerator, denominator, expected):
    assert expected == main.divide(numerator, denominator)



@pytest.mark.parametrize("numerator, denominator", [
    # we here are focusing on checking if the output is positive, we don't need to check if the sub operation itself is correct, it's already checked on the last test function, so no need for expected
    (2, 0),
    (10, 0),
    (3, 0)
])
def test_divide_by_zero_raises_error(numerator, denominator):
    # By using pytest.raises, you're saying:
    # “Yes, I expect this error — it means the function works correctly.”
    # match message must be the same as the error message of the error on the main function
    with pytest.raises(ValueError, match="Can't divide by zero"):  
        main.divide(numerator, denominator)



@pytest.mark.parametrize("statement, expected", [
    ("my name is islam", "My Name Is Islam"),
    ("hello world", "Hello World"),
    ("PYTHON is FUN", "Python Is Fun"),
    ("", ""),
])
def test_capitalize_various_cases(statement, expected):
    assert expected == main.capitalize_each_word(statement)



@pytest.fixture
def user():
    # If you change (mutate) this dictionary inside one test, it may affect another test if pytest reuses the same object 
    # If you're working with mutable data (like dict, list), return a copy so each test gets a fresh one
    return {"name": "islam", "age": 30}.copy()

def test_define_user(user):
    assert main.define_user(user) == "Username is ISLAM, user's age is 30"

def test_define_user_check_name_not_empty(user):
    assert len(user['name']) > 0

def test_define_user_check_age_is_positive(user):
    assert user['age'] > 0





"""
Notes:
    - How did adding __init__.py to tests/ fix the import?
        - The Python interpreter now recognizes the tests folder as a real Python module or package.
        - This improves how Python resolves relative imports
        - By default, Python doesn’t know where to find main.py unless your current directory is added to the import path (sys.path).
        - When you add __init__.py, it enables Python to walk back up the directory tree more intelligently to find main.py in the parent folder.

        - Think of __init__.py as a way of saying:
        "Hey Python, treat this folder as part of the project — so relative imports from here are allowed."

        
    - Why can’t one decorator apply to two tests?
        - Because Python decorators (like @pytest.mark.parametrize) are just functions that wrap a single function.
        - They don’t magically apply to everything below — only the next function.

    
"""
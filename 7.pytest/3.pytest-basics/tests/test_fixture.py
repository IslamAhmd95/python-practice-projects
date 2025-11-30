import pytest


"""
Exercise 1 — basic fixture
Create a fixture message returning "Hello pytest"then create two tests using it.
"""

@pytest.fixture
def message():
    return "Hello pytest"

def test_message_exists(message):
    assert len(message) > 0

def test_message(message):
    assert message == "Hello pytest"



"""
Exercise 2 — fixture + yield
Create a fixture:
    prints "Start"
    yields a dictionary {"x": 5}
    prints "End"
Write two tests that use it.
"""
@pytest.fixture
def db():
    print('Start') # <--- Added "Start" print
    data = {"x": 5}
    yield data # <--- Yielding the dictionary
    print('End') # <--- Added "End" print

def test_db_has_correct_key(db):
    assert "x" in db

def test_db_has_correct_value(db):
    assert db["x"] == 5


"""
Exercise 3 — parametrized fixture
Create a fixture that returns values: "red", "blue", "green", create a test that checks:
"""
@pytest.fixture(params=["red", "blue", "green"]) # 3 tests will run.
def color(request):
    return request.param

def test_color(color):
    assert color in ["red", "blue", "green"]


"""
Exercise 4 — fixture uses another fixture
Create a fixture that returns a value from another fixture, create a test that checks:
"""

@pytest.fixture
def x():
    return 5

@pytest.fixture
def square(x):
    return x * x

@pytest.fixture
def double(square):
    return square * 2

def test_double(double):
    assert double == 50


import pytest


# Example 1
@pytest.mark.parametrize("num", [2, 4, 6])  # runs 3 tests
def test_is_even(num):
    assert num % 2 == 0


# Example 2
@pytest.mark.parametrize("a, b, result", [
    (1, 2, 3),
    (2, 4, 6),
    (0, 0, 0),
    (-1, -2, -3)
])
def test_add(a, b, result):
    assert a + b == result


# Example 3
@pytest.mark.parametrize(
    "letter",
    ["a", "b", "c"],
    ids=["first", "second", "third"]  # Third Argument (Optional, ids=["first", "second", "third"]): This is a list of custom strings used to generate a unique, human-readable name for each parameterized test case when pytest reports the results.
)
def test_letter(letter):
    assert letter in ["a", "b", "c"]


# Example 4 : use fixture with paramterizing
@pytest.fixture(params=[20, 30, 40])
def number(request):
    return request.param

def test_number(number):
    assert number > 10


# Example 5: Parametrizing Both Fixture + Test Together
@pytest.fixture(params=[1, 2])
def a(request):
    return request.param

@pytest.mark.parametrize("b", [10, 20, 30])
def test_multiply(a, b):  # runs 6 times
    assert a * b >= 10


# Example 6: Parametrizing Test Classes
@pytest.mark.parametrize("x", [1, 2, 3])
class TestNumbers:
    def test_positive(self, x):
        assert x > 0

    def test_square(self, x):
        assert x * x >= x


# Example 7: Parametrize with a list of dictionaries (very useful in API testing)
test_cases = [
    {"username": "user1", "valid": True},
    {"username": "", "valid": False},
    {"username": None, "valid": False},
]

@pytest.mark.parametrize("user", test_cases)
def test_user(user):
    username = user['username']
    valid = user['valid']

    assert (username is not None and username != '') == valid


# Example 8: Parametrizing Functions That Return Data
def multiply(a, b):
    return a * b

@pytest.mark.parametrize("a, b, result", [
    (2, 3, 6),
    (-1, 5, -5),
    (10, 0, 0)
])
def test_multiply(a, b, result):
    assert multiply(a, b) == result



# -----------------------------------------------------------------

"""
# Exercise 1 - Test a function is_positive(n) with values:
5 → True
0 → False
-3 → False
"""

def is_positive(n):
    return n > 0

@pytest.mark.parametrize(
        "n, expected",
        [
            (5, True),
            (0, False),
            (-3, False)
        ],
        ids=["positive", "zero", "negative"]
)
def test_is_positive(n, expected):
    assert is_positive(n) == expected



"""
Exercise 2 — Parametrized Fixture

Create a fixture returning 3 values:
"small", "medium", "large".

Test that each string has length ≥ 4.
"""
@pytest.fixture(params=["small", "medium", "large"])
def size(request):
    return request.param

def test_size(size):
    assert len(size) >= 4



"""
Exercise 4 — Skip specific cases

Parametrize numbers:
[1, 2, 3, 4, 5]

Skip the test ONLY for number 3.
"""
def is_positive(n):
    return n > 0

@pytest.mark.parametrize(
    "number",
    [
        1,
        2,
        pytest.param(3, marks=pytest.mark.skip(reason="skip number 3")),
        4,
        5
    ],
    ids=["one", "two", "three_skipped", "four", "five"]
)
def test_numbers(number):
    assert is_positive(number) is True
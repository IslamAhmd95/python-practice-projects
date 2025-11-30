import pytest
from exercises.exercise1_basic import *


@pytest.mark.parametrize("x, y, result", [
    (1, 2, 3),
    (-1, -2, -3),
    (1, -1, 0)
])
def test_add(x, y, result):
    assert add(x, y) == result


@pytest.fixture(params=[(1, False), (2, True)])
def even_test_cases(request):
    return request.param


def test_is_even(even_test_cases):
    assert is_even(even_test_cases[0]) == even_test_cases[1]


@pytest.mark.parametrize("s, expected", [
    ("islam", "malsi"),
    ("i", "i")
])
def test_reverse_string(s, expected):
    assert reverse_string(s) == expected


def test_reverse_string_empty_raises():
    with pytest.raises(ValueError, match="Please enter a valid string"):
        reverse_string("")


@pytest.mark.parametrize("numbers, expected", [
    ([1, 5, 3, 9, 2], 9),  # normal list
    ([-5, -1, -10, -3], -1),  # negative numbers
    ([7, 10, 5, 10, 3], 10),  # list with duplicate max
    ([42], 42)  # single element
])
def test_find_max(numbers, expected):
    assert find_max(numbers) == expected

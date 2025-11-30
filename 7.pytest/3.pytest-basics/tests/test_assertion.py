import pytest

from assertion import *


def test_a_greater_than_b():
    assert max_of_two(4, 3) == 4


def test_b_greater_than_a():
    assert max_of_two(3, 4) == 4


def test_a_equal_b():
    with pytest.raises(ValueError, match="a can't be equal to b"):
        max_of_two(4, 4)


def test_filter_even_empty_raises_error():
    with pytest.raises(ValueError, match="List can't be empty"):
        filter_even([])


def test_filter_even_functionality():
    assert filter_even([2, 4, 6]) == [2, 4, 6]
    assert filter_even([1, 3, 5]) == []
    assert filter_even([1, 2, 3, 4, 5]) == [2, 4]


def test_get_age_all():
    with pytest.raises(KeyError, match="Missing age"):
        get_age({"name": "Islam"})
    
    assert get_age({"name": "Islam", "age": 30}) == 30
     
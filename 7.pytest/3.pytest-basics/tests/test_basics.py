import pytest

from basics import *




def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(3, 0) == 0


def test_multiply_by_one():
    assert multiply(3, 1) == 3


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)


def test_square_positive():
    assert square(3) == 9


def test_square_negative():
    assert square(-3) == 9


def test_square_zero():
    assert square(0) == 0


def test_is_even():
    assert is_even(6) is True


def test_is_odd():
    assert is_even(5) is False


def test_is_negative_even():
    assert is_even(-6) is True


def test_is_negative_odd():
    assert is_even(-5) is False


def test_reverse_string():
    assert reverse_string("ISLAM") == "MALSI"


def test_reverse_empty_string():
    with pytest.raises(ValueError, match="Please enter a valid string"):
        reverse_string('')  # better and cleaner not using assert


def test_reverse_single_character():
    assert reverse_string('s') == 's'


def test_reverse_string_with_spaces():
    assert reverse_string('Islam Ahmed') == 'demhA malsI'


def test_error_message():
    with pytest.raises(ValueError) as e:
        raise ValueError("Invalid")
    assert "Invalid" in str(e)


def test_floats():
    # assert 0.1 + 0.2 == 0.3  # fails
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_custom_message():
    age = 19
    assert age >= 18, "Age must be greater or equal then 18"
import pytest

from organizing import *


@pytest.fixture
def math_operations():
    return MathOperations()


class TestMathOperations:
    def test_add(self, math_operations):
        assert math_operations.add(1, 2) == 3

    def test_subtract(self, math_operations):
        assert math_operations.subtract(1, 2) == -1

    def test_multiply(self, math_operations):
        assert math_operations.multiply(1, 2) == 2

    def test_divide_by_zero(self, math_operations):
        with pytest.raises(ZeroDivisionError):
            math_operations.divide(1, 0)

    def test_divide(self, math_operations):
        assert math_operations.divide(1, 2) == pytest.approx(0.5)


@pytest.fixture
def user():
    return GetUser("Islam", 30)


class TestGetUser:
    def test_introduce_user(self, user):
        assert user.introduce_user() == "User's name is Islam and age is 30 years old."


@pytest.fixture
def string_helpers():
    return StringHelpers()


class TestStringHelpers:

    def test_reverse_empty_name(self, string_helpers):
        with pytest.raises(ValueError, match="String input cannot be empty."):
            string_helpers.reverse_name('')

    def test_reverse_name(self, string_helpers):
        assert string_helpers.reverse_name('Islam') == 'malsI'

    def test_palindrome_empty_string(self, string_helpers):
        with pytest.raises(ValueError, match="String input cannot be empty."):
            string_helpers.palindrome('')

    def test_palindrome(self, string_helpers):
        assert string_helpers.palindrome("eye") == True
        assert string_helpers.palindrome("bla") == False

    def test_check_starts_with_upper_case_empty_string(self, string_helpers):
        with pytest.raises(ValueError, match="String input cannot be empty."):
            string_helpers.check_starts_with_upper_case('')

    def test_check_starts_with_upper_case(self, string_helpers):
        assert string_helpers.check_starts_with_upper_case('Islam') is True
        assert string_helpers.check_starts_with_upper_case('islam') is False


# no need to implement fixture for FileOperations, since it's not implemented yet
@pytest.mark.skip(reason="Not implemented yet")
class TestFileOperations:
    def test_read(self):
        pass
    
    def test_write(self):
        pass
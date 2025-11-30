import pytest

from exercises.exercise3_parametrize import *



@pytest.mark.parametrize(
    "name", [
        123, None, True
    ]
)
def test_normalize_name_type_error(name):
    with pytest.raises(TypeError, match="Name must be a string"):
        normalize_name(name)

@pytest.mark.parametrize("name, expected", [
    ('Alice', 'alice'),
    ('BoB', 'bob'),
    (' Carol ', 'carol'),
    ('david ', 'david')
])
def test_normalize_name(name, expected):
    assert normalize_name(name) == expected



# Optional: Fixture to create a Temperature instance with a known value
@pytest.fixture
def temp_37():
    return Temperature(37)

class TestTemperature:

    # Test 1: to_fahrenheit method
    @pytest.mark.parametrize("celsius, expected_f", [
        (0, 32),
        (100, 212),
        (-40, -40),
        (37, 98.6)
    ])
    def test_to_fahrenheit(self, celsius, expected_f):
        temp = Temperature(celsius)
        assert temp.to_fahrenheit() == pytest.approx(expected_f)

    # Test 2: is_freezing method
    @pytest.mark.parametrize("celsius, expected_bool", [
        (0, True),
        (-40, True),
        (100, False),
        (0.1, False)
    ])
    def test_is_freezing(self, celsius, expected_bool):
        temp = Temperature(celsius)
        assert temp.is_freezing() is expected_bool


# exercise3_parametrize.py


def normalize_name(name: str):
    """Return a cleaned lowercase name without extra spaces."""
    if not isinstance(name, str):
        raise TypeError("Name must be a string")

    return name.strip().lower()


class Temperature:
    """Represents temperature in Celsius."""

    def __init__(self, celsius: float):
        self.celsius = celsius

    def to_fahrenheit(self) -> float:
        return (self.celsius * 9 / 5) + 32

    def is_freezing(self) -> bool:
        return self.celsius <= 0

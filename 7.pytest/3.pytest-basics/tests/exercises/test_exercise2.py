import random

import pytest

from exercises.exercise2_fixtures import *


@pytest.fixture
def memory_val():
    return random.randint(0, 10)

@pytest.fixture
def calc():
    return Calculator()

class TestCalculator:
    def test_remember(self, calc, memory_val):
        calc.remember(memory_val)
        assert calc.recall() == memory_val

    def test_clear(self, calc):
        calc.clear()
        assert calc.recall() == 0



@pytest.fixture
def users():
    return {
        "Islam": {"email": "islam@gmail.com"},
        "ahmed": {"email": "ahmed@gmail.com"},
    }


@pytest.fixture
def user_db(users):
    db = UserDB()

    for username, data in users.items():
        db.add_user(username, data["email"])

    yield db

    db.clear()

class TestUserDB:
    def test_add_user(self, user_db):
        user_db.add_user("nour", "nour@gmail.com")
        assert user_db.get_user("nour") == {"email": "nour@gmail.com"}

    def test_add_user_user_exists(self, user_db):
        with pytest.raises(ValueError, match="User already exists"):
            user_db.add_user("Islam", "islam@gmail.com")


    def test_clear(self, user_db):
        user_db.clear()
        assert user_db.users == {}
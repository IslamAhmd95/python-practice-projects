from UserManager import UserManager
import pytest

@pytest.fixture
def user_manager():
    """Creates a fresh instance of of UserManager before each test"""
    return UserManager()


@pytest.mark.parametrize("username, email", [
    ("islam", "islam@gmail.com"),
    ("ahmed", "ahmed@gmail.com"),
    ("saad", "saad@gmail.com"),
])
def test_add_user_various_cases(user_manager, username, email):
    result = user_manager.add_user(username, email)
    assert result is True
    assert user_manager.get_user(username) == email


def test_add_user_duplicate_users(user_manager):
    user_manager.add_user("islam", "islam@gmail.com")
    with pytest.raises(ValueError, match="User already exists"):
        user_manager.add_user("islam", "islam@gmail.com")


def test_get_nonexistent_user_returns_none(user_manager):
    assert user_manager.get_user("notExistent") is None
import pytest  # pyright: ignore[reportMissingImports]
from Database import Database


"""
- In pytest, fixture scopes control how often the fixture is created and how long it lives.

- Fixture score options:

| Scope        | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| `"function"` | (default) New fixture created **for each test function**                   |
| `"class"`    | One fixture per test **class**                                             |
| `"module"`   | One fixture per **test file/module**                                       |
| `"package"`  | One fixture per **package (directory with __init__.py)** (rarely used) |
| `"session"`  | One fixture **shared across the whole test session**                       |

"""


@pytest.fixture(scope="function")
def db():
    """
    Fixture that provides a fresh Database instance for each test.
    The setup code goes before 'yield'.
    The teardown code (optional cleanup/logging) goes after 'yield'.
    """
    # Setup: create a fresh Database instance
    database = Database()
    print("\n[Setup] Creating a new Database instance")
    
    yield database  # This is where the test runs, with 'database' available to it

    # Teardown: logic that runs *after* the test finishes
    print("[Teardown] Test finished. Database cleared/logged/etc.")


def test_add_user(db):
    db.add_user(1, "islam")
    assert db.get_user(1) == "islam"

def test_add_user_duplicate_users(db):
    db.add_user(1, "islam")
    with pytest.raises(ValueError, match="User already exists"):
        db.add_user(1, "islam")

def test_get_nonexistent_user_returns_none(db):
    assert db.get_user(1) is None

def test_del_user(db):
    db.add_user(1, "islam")
    db.delete_user(1)
    assert db.get_user(1) is None

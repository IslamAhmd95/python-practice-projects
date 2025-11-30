import pytest

@pytest.fixture(scope="session")  # can be used in any test file within the session without import it
def db():
    print("Connect to db")
    yield "DB Object"
    print("Close db")


@pytest.fixture
def user():
    return {"id": 1, "name": "Islam"}

@pytest.fixture
def products():
    return ["laptop", "phone", "camera"]


# fixture chaining
@pytest.fixture
def base_number():
    return 10

@pytest.fixture
def double_number(base_number):  # used inside `test_working_with_conftest.py`
    return base_number * 2


@pytest.fixture
def open_file():
    print("Opening file")
    with open('test.txt', 'w') as f:
        yield f
    print("Closing file")

# parametrized fixture and use it anywhere
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param


@pytest.fixture(autouse=True)  # run with each test
def debug():
    print(">> Running a test...")



@pytest.fixture(scope="session")  # provide global settings to all tests
def settings():
    return {
        "BASE_URL": "https://api.example.com",
        "API_KEY": "12345"
    }


@pytest.fixture(autouse=True)  # run with each test
def setup_env(monkeypatch):
    monkeypatch.setenv('MODE', 'test')


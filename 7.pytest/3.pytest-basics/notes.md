## basics

    - Test file names must be:
        - Start with: test_*.py
        - OR end with: *_test.py
    - Test functions must start with test_
    - `pytest` command runs tests of the project with a more detailed output
    - `pytest -q` command reduces the amount of output it prints to the console while running your tests.
    - no need to use `assert` inside `pytest.raises`


## Assertions


## Organizing tests

    - Class name starts with Test
    - Class must NOT have an __init__ method
    - Classes help when:
        - You want to group logically related tests
            - Ex:
                `
                class TestLogin:
                    def test_valid_credentials(self):
                        assert login("user", "pass") == True

                    def test_invalid_username(self):
                        assert login("wrong", "pass") == False

                    def test_invalid_password(self):
                        assert login("user", "wrong") == False

                `
        - You want to apply fixtures to a whole group
        - You want better test output structure
        - EX:
            `
                tests/
                test_math.py
                test_strings.py

                test_strings.py output:
                TestStringFunctions::test_upper PASSED
                TestStringFunctions::test_isdigit PASSED

            `
        - Running Specific Classes or Methods
            - run singe class -> `pytest tests/test_math.py::TestMath`
            - run single test -> `pytest tests/test_math.py::TestMath::test_add`
        - use `@pytest.mark.skip(reaso="")` decorator to skip testing classes or functions


## fixture

    - fixture is a reusable function that provides “setup” for your tests.
        - Open a database connection
        - Prepare a test user
        - Create a temporary file
        - Provide a fake API client
        - Provide sample data
        - Configure environment variables
    - fixture scopes
        - function 'default'
        - class
        - module
        - session
    - Autouse Fixtures `@pytest.fixture(autouse=True)`, runs automatically with every test without adding it to the parameters
    - parametrized fixtures: create a fixture that gives different values to tests.
    - Fixtures Can Use Other Fixtures


## parametrizing

    - parametrizing means “Run the same test several times, but with different inputs and expected results.”


## markers

    - Markers = labels you attach to tests for special behavior.
    - I have to register Markers in pytest.ini


## conftest

    - conftest.py is a special pytest file used to share:
        - fixtures
        - hooks
        - configs
        - helper functions
        across your entire test suite without importing anything.
        🟢 You don't import from conftest.py
        🟢 pytest automatically discovers it
        🟢 It makes your tests clean and avoids duplication
    - You can have multiple levels of conftest.py
        - fixtures in tests/conftest.py → available everywhere
        - fixtures in tests/api/conftest.py → available only inside api/
        - fixtures in tests/db/conftest.py → available only inside db/


## mocking

    - Mocking in pytest means replacing real code with fake/stub code during testing.

    - Why ? Because in tests we don’t want to:
        - call real APIs
        - send real emails
        - connect to real databases
        - use real time.sleep
        - rely on real file systems
        - depend on randomness
    
    - Use monkeypatch when you can assign simple attributes
    - Use mock.patch for advanced mocks (return values, asserts, side effects)
    - `monkeypatch` for Environment variables, file system access.
    - `unittest.mock.patch` for Replacing a complex function or method on a class or module with a simple return value.


## running tests

    - Files starting with test_*.py
    - Files ending with *_test.py
    - Functions starting with test_
    - Classes starting with Test
    - `pytest -v` for detailed output
    - `pytest tests/test_api.py` runs specific file
    - `pytest tests/test_api.py::test_get_user` runs specific test function
    - `pytest tests/test_api.py::TestUsers::test_create_user` runs specific test function inside test class
    - `pytest -x` stops after first failure
    - `pytest -k "specific_keyword"` Run tests that contain a keyword in the name
        - `pytest -k "login and success"` "login and success" is the keyword
        - `pytest -k "not slow"` exclude "slow" keyword 
    - `pytest -s` Output is always shown immediately, regardless of whether the test passes or fails, likes prints and others


## pytest.ini / pyproject.toml

    - both pytest.ini and pyproject.toml primarily serve the same job of storing configuration settings for your test suite.
    - pytest.ini is an old format of configuration
        - Ex: 
            `
            [pytest]
            addopts = -v --tb=short -p no:warnings
            testpaths = tests
            python_files = test_*.py
            python_functions = test_*
            python_classes = Test*
            markers =
                slow: slow tests
                api: tests that use API
                db: database tests
            `
        - now providing the above adopts, i can only run `pytest` and the above adopts will be added to the command `pytest`

    - pyproject.toml — The modern alternative: Modern Python projects prefer putting config inside pyproject.toml.
        - Ex:
            `
            [tool.pytest.ini_options]
            addopts = "-v --tb=short -p no:warnings"
            testpaths = ["tests"]
            python_files = ["test_*.py", "*_test.py"]

            markers = [
                "slow: slow tests",
                "api: API tests",
                "db: database tests"
            ]
            `

    - How pytest decides which config to load
        - Order priority:
            - pyproject.toml
            - pytest.ini
            - tox.ini
        Pytest uses the first file it finds.


## coverage

    - Test coverage = how much of your code is actually tested.
    - If your project has 100 lines of code and your tests execute 70 of them: coverage = 70%
    - Coverage helps answer:
        - Did my tests run all functions?
        - Did they run all branches (if/else)?
        - Are there dead areas in my code?
    Coverage tells you what parts of your code were executed by tests and highlights what was not executed.
    - you must install `coverage` or `pytest-cov` to monitor my app tests coverage

    - `coverage run -m pytest` run tests with coverage
    - `coverage report` show coverage report
    - `coverage html` creates a folder htmlcov/ with index.html file inside which shows  a beautiful UI showing:
        - lines tested (green)
        - lines NOT tested (red)
        - branches missed

    - `pytest --cov=app` tests code inside app/ folder using pytest-cov
    - `pytest --cov=backend --cov-report=html` generates html
    - `addopts = --cov=backend --cov-report=term-missing` - I can add this line to pytest.ini or pyproject.toml 'just add quotation' then just run `pytest` which automatically includes coverage and also shows which lines are missing tests. 
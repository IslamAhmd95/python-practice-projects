import api
from unittest.mock import patch
import pytest  # pyright: ignore[reportMissingImports]


# Define the @patch decorators in the same order as your real function uses the dependencies,
# then reverse that order in your test function parameters.
@patch('api.logging.info')   # used FIRST in real function
@patch('api.requests.get')   # Replace `requests.get` inside api module
# "In the scope of this test, replace requests.get inside api module with a mock object, and give it to me as `mock_get`, so `mock_get` is the same as `requests.get`"
def test_get_user_data(mock_get, mock_log):  
    mock_response = mock_get.return_value   # `mock_get.return_value` simulate `response`

    # If you don’t explicitly mock the status_code, the mock default will be a MagicMock object — not the integer 200. So the condition will be true, and it’ll raise the error unexpectedly.
    mock_response.status_code = 200

    # Arrange: Mock the .json() method to return fake data, it's equal to `return response.json()`
    mock_response.json.return_value = {"name": "islam", "age": 30}    

    # This runs your real logic that calls requests.get().json(), but now it’s hitting the mocked version `@patch('api.requests.get') `.
    result = api.get_user_data('https://api.example.com/users/1')

    # check if the result of running the function is the same as the api response
    # You check that the return value of your function is exactly the fake data you configured.
    assert result['name'] == 'islam' and result['age'] == 30

    # "Check that the mock function logging.info() was called once, and exactly with the argument 'Fetching data from https://api.example.com/users/1'."
    mock_log.assert_called_with('Fetching data from https://api.example.com/users/1')



@patch('api.requests.get')
def test_get_user_data_status_code(mock_get):
    mock_get.return_value.status_code = 500

    with pytest.raises(Exception, match="Failed to fetch data"):
        api.get_user_data('https://api.example.com/users/1')


"""
What is Mock?
    Mocking is a technique used in testing to:
        - Replace real objects or functions (like APIs, databases, file access) with fake (mocked) versions that simulate behavior


Related mock assertions:

| Method                         | Meaning                                                                 |
| ------------------------------ | ----------------------------------------------------------------------- |
| `assert_called()`              | Was it called at least once?                                            |
| `assert_called_once()`         | Was it called **exactly once**?                                         |
| `assert_called_with(...)`      | Was it called (at least once), and did the **last call** match exactly? |
| `assert_called_once_with(...)` | Called **once and only once**, with exact arguments                     |
| `assert_not_called()`          | Was it **never called**?                                                |

"""
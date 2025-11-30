import pytest

from exercises.exercise5_mocking import *


def test_fetch_user(user, mocker):  # mocker is a built-in pytest fixture
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = user

    mock_get = mocker.patch(
        "exercises.exercise5_mocking.requests.get", return_value=mock_response)

    assert fetch_user(1) == user

    expected_url = f"https://api.example.com/users/1"
    mock_get.assert_called_once_with(expected_url)


def test_write_to_file(tmp_path):

    # 1. SETUP: Create a temporary file path
    # tmp_path is a Path object; the / operator creates a new file path inside it.
    file_path = tmp_path / "test.json"

    data = {"name": "Islam"}
    result = write_to_file(file_path, data)

    assert result is True

    actual_content = file_path.read_text()

    assert actual_content == '{"name": "Islam"}'


def test_get_timestamp_with_mock(mocker):
    """Test get_timestamp by mocking time.time()."""
    # Mock time.time() to return a fixed timestamp
    mock_time = mocker.patch(
        "exercises.exercise5_mocking.time.time", return_value=1234567890.5)

    result = get_timestamp()

    # Should return the integer value of the mocked timestamp
    assert result == 1234567890
    mock_time.assert_called_once()


def test_get_timestamp_returns_int():
    """Test get_timestamp returns an integer (without mocking)."""
    result = get_timestamp()

    assert isinstance(result, int)
    assert result > 0


def test_get_timestamp_is_reasonable(mocker):
    """Test get_timestamp returns a reasonable UNIX timestamp."""
    # Mock time.time() to return a specific known value
    mocker.patch("exercises.exercise5_mocking.time.time",
                 return_value=1609459200)  # 2021-01-01 00:00:00 UTC

    result = get_timestamp()

    # Verify it's the expected timestamp
    assert result == 1609459200


@pytest.fixture
def email_service():
    return EmailService()


def test_send_email_success(email_service, mocker):
    """Test send_email returns correct response."""
    # Mock time.sleep to avoid 0.2s delay in tests
    mocker.patch("exercises.exercise5_mocking.time.sleep")

    result = email_service.send_email(
        "user@example.com", "Test Subject", "Test Body")

    assert result == {"status": "sent", "to": "user@example.com"}


def test_send_email_skips_sleep(email_service, mocker):
    """Test send_email doesn't actually sleep (mocked)."""
    mock_sleep = mocker.patch("exercises.exercise5_mocking.time.sleep")

    email_service.send_email("user@example.com", "Subject", "Body")

    # Verify time.sleep was called with 0.2 seconds
    mock_sleep.assert_called_once_with(0.2)


def test_send_email_multiple_calls(email_service, mocker):
    """Test send_email with multiple recipients."""
    mocker.patch("exercises.exercise5_mocking.time.sleep")

    result1 = email_service.send_email(
        "alice@example.com", "Hello", "Hi Alice")
    result2 = email_service.send_email("bob@example.com", "Hello", "Hi Bob")

    assert result1["to"] == "alice@example.com"
    assert result2["to"] == "bob@example.com"

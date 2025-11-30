from unittest.mock import patch, Mock
from mocking import total_price, notify, EmailSender, fetch


#  Example 1 : mocking function

def test_total_price():
    with patch('mocking.get_price') as mock_price:  # We don’t want real get_price() to run and no external API call
        mock_price.return_value = 20
        assert total_price(3) == 60


# another way

def test_total_price_sec_way(monkeypatch):
    def fake_get_price():
        return 20
    
    monkeypatch.setattr("mocking.get_price", fake_get_price)
    assert total_price(3) == 60

    
# ----------------------------------------

#  Example 2 : mocking class

def test_notify():
    fake_sender = Mock()
    fake_sender.send.return_value = True

    result = notify(fake_sender, "Islam")

    assert result is True

    fake_sender.send.assert_called_once_with("Islam", "Welcome!")


# another way using mock.patch.object

with patch.object(EmailSender, "send", return_value=True):
    sender = EmailSender()
    assert sender.send("Islam", "Hi") is True


# ----------------------------------------

# Example 3: Mocking external HTTP requests

def test_fetch():
    fake_response = Mock()
    fake_response.status_code = 200

    with patch("mocking.requests.get", return_value=fake_response):
        assert fetch() == 200
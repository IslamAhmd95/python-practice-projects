import pytest

from exercises.exercise4_markers import *


@pytest.mark.fast
@pytest.mark.parametrize("x, y, result", [
    (1, 2, 3),
    (3, 2, 5),
])
def test_fast_add_positive(x, y, result):
    assert fast_add(x, y) == result


@pytest.mark.fast
@pytest.mark.parametrize("x, y, result", [
    (-1, -2, -3),
    (-3, -2, -5),
])
def test_fast_add_negative(x, y, result):
    assert fast_add(x, y) == result


@pytest.mark.slow
@pytest.mark.parametrize("x, y, result", [
    (1, 2, 2),
    (3, 2, 6),
])
def test_multiply_positive(x, y, result):
    assert slow_multiply(x, y) == result


@pytest.mark.slow
@pytest.mark.parametrize("x, y, result", [
    (-1, -2, 2),
    (-3, -2, 6),
    (-3, 5, -15),
])
def test_multiply_negative(x, y, result):
    assert slow_multiply(x, y) == result


@pytest.fixture
def bank():
    return BankAccount()


class TestBankAccount:

    @pytest.mark.bank
    @pytest.mark.parametrize("amount", [-10, -20])
    def test_deposit_negative(self, bank, amount):
        with pytest.raises(ValueError, match="Deposit must be positive"):
            bank.deposit(amount)

    @pytest.mark.bank
    @pytest.mark.parametrize("amount", [10, 20])
    def test_deposit_positive(self, bank, amount):
        current_balance = bank.get_balance()
        assert bank.deposit(amount) == current_balance + amount

    @pytest.mark.bank
    @pytest.mark.parametrize("amount", [1000, 2000])
    def test_withdraw_negative(self, bank, amount):
        with pytest.raises(ValueError, match="Insufficient funds"):
            bank.withdraw(amount)

    @pytest.mark.bank
    @pytest.mark.parametrize("balance, amount, result", [(100, 10, 90), (200, 20, 180)])
    def test_withdraw_positive(self, bank, balance, amount, result):
        bank.deposit(balance)
        assert bank.withdraw(amount) == result

    def test_get_balance_initial(self, bank):
        assert bank.get_balance() == 0

    @pytest.mark.bank
    def test_deposit_zero_raises(self, bank):
        with pytest.raises(ValueError, match="Deposit must be positive"):
            bank.deposit(0)

    @pytest.mark.bank
    @pytest.mark.parametrize("balance, amount, expected", [(100, 100, 0), (50, 50, 0)])
    def test_withdraw_exact_balance(self, bank, balance, amount, expected):
        bank.deposit(balance)
        assert bank.withdraw(amount) == expected
        assert bank.get_balance() == expected

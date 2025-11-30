import os

from typing import Literal


def test_get_data(db):
    assert db == "DB Object"

def test_user_name(user):
    assert user['name'] == "Islam"

def test_products_len(products):
    assert len(products) == 3


def test_double_number(double_number):
    assert double_number == 20

def test_write_and_verify(open_file):
    open_file.write("Hello World")
    open_file.flush()  # flush means force saving the data to the file
    with open('test.txt', 'r') as f:
        assert f.read() == "Hello World"


def test_numbers(number):
    assert number > 0


def test_api_config(settings):
    assert settings["BASE_URL"].startswith("https")


def test_env():
    os.getenv('MODE') == 'test'  # This is True during the test

"""
What monkeypatch Does
    The term "monkeypatching" is a general programming concept that refers to dynamically replacing attributes or methods at runtime. Pytest's monkeypatch fixture makes this process safe and easy specifically for testing.

It's essentially a tool for making temporary, reversible changes (like substituting functions, overriding global variables, or manipulating environment variables) that are automatically undone after the test completes.

Key Features
    - Temporary Changes: Any change made using monkeypatch is local to the current test or fixture.
    - Automatic Reversal: After the test or the fixture using it finishes, monkeypatch automatically cleans up and restores the original state of the code, environment, or objects. This prevents tests from interfering with each other.
    - Scope: It works across functions, modules, classes, and even the operating system environment.
"""

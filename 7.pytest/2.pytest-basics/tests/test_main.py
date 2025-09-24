import main
import pytest


@pytest.mark.parametrize("x, y, expected", [
    (1, 3, 4),
    (2, 4, 6),
    (3, 7, 10),
    (-3, 7, 4),
])
def test_add_various_cases(x, y, expected):
    assert expected == main.add(x, y)


@pytest.mark.parametrize("numerator, denominator, expected", [
    (3, 3, 1),
    (4, 2, 2),
    (20, 5, 4)
])
def test_divide_various_cases(numerator, denominator, expected):
    assert expected == main.divide(numerator, denominator)


@pytest.mark.parametrize("numerator, denominator", [
    (3, 0),
    (4, 0),
    (20, 0)
])
def test_divide_by_zero_raises_error(numerator, denominator):
    with pytest.raises(ValueError, match="Can't divide by zero"):
        main.divide(numerator, denominator)


def test_report(capsys): # capsys is passed automatically — it's a built-in pytest fixture that captures console output.

    # Call the real function — it prints "Hello, world!" to the screen, but pytest’s capsys is silently intercepting that output instead of letting it go to the terminal.
    main.report()

    # Use capsys to capture the printed output
    captured = capsys.readouterr()

    # captured.out holds the printed text (stdout)
    assert captured.out == "success\n"   #  \n because print statement adds it at the end
    # captured.err holds the printed text (stderr)
    assert captured.err == "error\n"  



"""
What does “capturing” mean in pytest?
    It means: holding printed output so you can inspect or test it later — instead of letting it go straight to the screen.
    Pytest uses it to:
        - Help you test what was printed
        - Keep test output clean (unless a test fails)
        - You can access the captured output using the capsys fixture
"""
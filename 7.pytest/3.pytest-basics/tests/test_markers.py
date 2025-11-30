import sys

import pytest


## Custom Markers (Categorizing Tests) + Running Tests With Markers (CLI)

@pytest.mark.slow   # run this custom mark with `pytest tests/test_markers.py -m slow`
def test_big_calc():
    assert 10000 + 10000 == 20000

@pytest.mark.fast  #  run this custom mark with `pytest -m fast`
def test_big_calc():
    assert 1 + 1 == 2

# `pytest -m "not slow"` run every thing except slow
# `pytest -m "slow or fast"`  run slow or fast marks


@pytest.mark.add
@pytest.mark.math
@pytest.mark.parametrize("a, b, result", [
    (1, 2, 3),
    (3, 4, 7)
])
def test_add(a, b, result):
    assert a + b == result

# `pytest -m "add and math"`  run tests with both marks



## Skipping a Test (@pytest.mark.skip)

@pytest.mark.skip(reason="Feature not implemented yet")  
def test_new_login():
    assert False



## Conditional Skip (skipif)

@pytest.mark.skipif(sys.platform=="win32", reason="don't run on windows")
def test_linux_only():
    assert True



## Expected Failure (xfail)

@pytest.mark.xfail(reason="This bug not fixed yet")  # means don't show the error since it is expected to be failed
def test_known_bug():
    assert 1/ 0 == 1
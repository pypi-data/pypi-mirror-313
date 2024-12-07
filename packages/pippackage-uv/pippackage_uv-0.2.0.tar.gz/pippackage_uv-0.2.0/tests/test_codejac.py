import pytest
from codestest.codes123.codesfile import codesFile
from codestest.codes456.testcodesfile import TstCodes


@pytest.fixture
def setup():
    tst = codesFile()
    return tst


@pytest.fixture
def setup2():
    tst = TstCodes()
    return tst


def test_div(setup):
    tst = setup
    assert tst.divide(4,2) == 2


def test_substract(setup):
    tst = setup
    assert tst.substract(4,2) == 2


def test_add(setup2):
    tst = setup2
    assert tst.add(2,2) == 4


def test_mul(setup2):
    tst = setup2
    assert tst.multiply(2,2) == 4
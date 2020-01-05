import pytest
from qidian.tools import RangeString


@pytest.fixture(scope="module")
def rs0():
    return RangeString("1")


@pytest.fixture(scope="module")
def rs1():
    return RangeString("-3")


@pytest.fixture(scope="module")
def rs2():
    return RangeString("1,3")


@pytest.fixture(scope="module")
def rs3():
    return RangeString("1-3")


@pytest.fixture(scope="module")
def rs4():
    return RangeString("3-")


@pytest.fixture(scope="module")
def rs5():
    return RangeString("-3,5,7-10,20-")


@pytest.fixture(scope="module")
def rs6():
    return RangeString("-")


@pytest.mark.parametrize("num, expect", [
    (0, False),
    (1, True),
    (2, False),
    (3, False),
])
def test_rs0(num, expect, rs0):
    assert rs0.match(num) == expect


@pytest.mark.parametrize("num, expect", [
    (0, True),
    (1, True),
    (2, True),
    (3, True),
    (4, False),
    (5, False),
])
def test_rs1(num, expect, rs1):
    assert rs1.match(num) == expect


@pytest.mark.parametrize("num, expect", [
    (0, False),
    (1, True),
    (2, False),
    (3, True),
    (4, False)
])
def test_rs2(num, expect, rs2):
    assert rs2.match(num) == expect


@pytest.mark.parametrize("num, expect", [
    (0, False),
    (1, True),
    (2, True),
    (3, True),
    (4, False),
])
def test_rs3(num, expect, rs3):
    assert rs3.match(num) == expect


@pytest.mark.parametrize("num, expect", [
    (0, False),
    (1, False),
    (2, False),
    (3, True),
    (4, True),
    (100, True),
])
def test_rs4(num, expect, rs4):
    assert rs4.match(num) == expect


@pytest.mark.parametrize("num, expect", [
    (0, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (8, True),
    (9, True),
    (10, True),
    (11, False),
    (20, True),
    (2000, True),
])
def test_rs5(num, expect, rs5):
    assert rs5.match(num) == expect


@pytest.mark.parametrize("num, expect", [
    (0, True),
    (2000, True),
    (100000, True)
])
def test_rs6(num, expect, rs6):
    assert rs6.match(num) == expect

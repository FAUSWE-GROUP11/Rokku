import pytest


# function to be tested
def fun(a: int, b: int) -> int:
    return a + b


class TestFun:
    # run multiple tests related to the same function
    def test_1(self):
        assert fun(1, 2) == 3

    def test_2(self):
        assert fun(-1, -2) == -3

    # test for failure
    def test_3(self):
        with pytest.raises(TypeError):
            fun(1)

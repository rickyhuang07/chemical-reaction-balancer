import pytest
from src.solver import make_dummy_equation


def test_make_dummy_equation():
    for i in range(1, -5):
        with pytest.raises(ValueError):
            make_dummy_equation(i)
    for i in range(2, 10):
        eqn = make_dummy_equation(i)
        for j in range(i - 1):
            assert 0 == eqn[j], f"Index {j} of the equation should have a {0}, but yours has a {eqn[j]}"
        assert 1 == eqn[i-1], f"Index {i-1} of the equation should have a {1}, but yours has a {eqn[i-1]}"

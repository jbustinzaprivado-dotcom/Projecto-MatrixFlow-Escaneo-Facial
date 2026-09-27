import pytest

from app.algorithms.errors import DimensionError
from app.algorithms.linear_algebra import linear_combination


def test_linear_combination():
    # c1*A + c2*B = 2*[1,2,3] + 3*[4,5,6] = [2,4,6] + [12,15,18] = [14,19,24]
    assert linear_combination([1, 2, 3], [4, 5, 6], 2, 3) == [14.0, 19.0, 24.0]


def test_linear_combination_coeficientes_negativos():
    assert linear_combination([1, 2], [1, 2], 1, -1) == [0.0, 0.0]


def test_linear_combination_dimensiones_incompatibles_ca06():
    with pytest.raises(DimensionError):
        linear_combination([1, 2, 3], [1, 2], 1, 1)

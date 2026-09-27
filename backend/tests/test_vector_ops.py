import pytest

from app.algorithms.errors import DimensionError
from app.algorithms.vector_ops import dot_product, scalar_multiply, subtract_vector, sum_vector


def test_sum_vector():
    assert sum_vector([1, 2, 3], [4, 5, 6]) == [5.0, 7.0, 9.0]


def test_subtract_vector():
    assert subtract_vector([5, 7, 9], [1, 2, 3]) == [4.0, 5.0, 6.0]


def test_scalar_multiply():
    assert scalar_multiply([1, 2, 3], 2) == [2.0, 4.0, 6.0]


def test_dot_product():
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32.0


def test_sum_vector_dimensiones_incompatibles_ca06():
    with pytest.raises(DimensionError):
        sum_vector([1, 2, 3], [1, 2])


def test_dot_product_dimensiones_incompatibles_ca06():
    with pytest.raises(DimensionError):
        dot_product([1, 2], [1, 2, 3])


def test_vector_vacio_es_invalido():
    with pytest.raises(DimensionError):
        sum_vector([], [])

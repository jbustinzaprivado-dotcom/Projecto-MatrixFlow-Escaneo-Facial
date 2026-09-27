import pytest

from app.algorithms.errors import DimensionError
from app.algorithms.matrix_ops import (
    add_matrix,
    multiply_matrix,
    scalar_multiply_matrix,
    subtract_matrix,
    transpose_matrix,
)


def test_add_matrix():
    assert add_matrix([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6.0, 8.0], [10.0, 12.0]]


def test_subtract_matrix():
    assert subtract_matrix([[5, 6], [7, 8]], [[1, 2], [3, 4]]) == [[4.0, 4.0], [4.0, 4.0]]


def test_multiply_matrix():
    assert multiply_matrix([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19.0, 22.0], [43.0, 50.0]]


def test_transpose_matrix():
    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]


def test_scalar_multiply_matrix():
    assert scalar_multiply_matrix([[1, 2], [3, 4]], 2) == [[2.0, 4.0], [6.0, 8.0]]


def test_add_matrix_dimensiones_incompatibles_ca06():
    with pytest.raises(DimensionError):
        add_matrix([[1, 2], [3, 4]], [[1, 2, 3]])


def test_multiply_matrix_dimensiones_incompatibles_ca06():
    # A es 2x2, B es 3x2: columnas de A (2) != filas de B (3)
    with pytest.raises(DimensionError):
        multiply_matrix([[1, 2], [3, 4]], [[1, 2], [3, 4], [5, 6]])


def test_multiply_matrix_no_es_conmutativa():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert multiply_matrix(a, b) != multiply_matrix(b, a)

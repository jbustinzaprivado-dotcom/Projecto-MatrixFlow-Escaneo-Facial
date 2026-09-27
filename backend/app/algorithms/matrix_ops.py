"""Matrices [PDF §11.2]."""

import numpy as np

from app.algorithms.errors import DimensionError


def validate_matrix(valores: list[list[float]]) -> np.ndarray:
    """[PDF §11.3: validate_matrix()]"""
    array = np.asarray(valores, dtype=float)
    if array.ndim != 2 or array.size == 0:
        raise DimensionError("La matriz debe tener al menos una fila y una columna.")
    return array


def validate_dimensions(a: np.ndarray, b: np.ndarray, *, multiplicacion: bool = False) -> None:
    """[PDF §11.3: validate_dimensions()]"""
    if multiplicacion:
        if a.shape[1] != b.shape[0]:
            raise DimensionError(
                f"Dimensiones incompatibles: A es {a.shape[0]}×{a.shape[1]} y B es "
                f"{b.shape[0]}×{b.shape[1]}; las columnas de A deben ser igual a las filas de B."
            )
        return
    if a.shape != b.shape:
        raise DimensionError(
            f"Dimensiones incompatibles: A es {a.shape[0]}×{a.shape[1]} y B es "
            f"{b.shape[0]}×{b.shape[1]}; deben tener el mismo tamaño."
        )


def add_matrix(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    ma, mb = validate_matrix(a), validate_matrix(b)
    validate_dimensions(ma, mb)
    return (ma + mb).tolist()


def subtract_matrix(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    ma, mb = validate_matrix(a), validate_matrix(b)
    validate_dimensions(ma, mb)
    return (ma - mb).tolist()


def multiply_matrix(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    ma, mb = validate_matrix(a), validate_matrix(b)
    validate_dimensions(ma, mb, multiplicacion=True)
    return (ma @ mb).tolist()


def transpose_matrix(a: list[list[float]]) -> list[list[float]]:
    ma = validate_matrix(a)
    return ma.T.tolist()


def scalar_multiply_matrix(a: list[list[float]], escalar: float) -> list[list[float]]:
    ma = validate_matrix(a)
    return (ma * escalar).tolist()

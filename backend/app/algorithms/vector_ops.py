"""Vectores [PDF §11.1]. Cada función es independiente, comprobable y reutilizable, tal como
pide el documento — no dependen de la base de datos ni de FastAPI."""

import numpy as np

from app.algorithms.errors import DimensionError


def validate_vector(valores: list[float]) -> np.ndarray:
    """[PDF §11.3: validate_vector()]"""
    array = np.asarray(valores, dtype=float)
    if array.ndim != 1 or array.size == 0:
        raise DimensionError("El vector debe tener al menos un valor.")
    return array


def validate_dimensions(a: np.ndarray, b: np.ndarray) -> None:
    """[PDF §11.3: validate_dimensions()]"""
    if a.shape != b.shape:
        raise DimensionError(
            f"Dimensiones incompatibles: A tiene {a.size} valores y B tiene {b.size}; "
            "deben tener el mismo tamaño (PDF: criterio CA-06)."
        )


def sum_vector(a: list[float], b: list[float]) -> list[float]:
    va, vb = validate_vector(a), validate_vector(b)
    validate_dimensions(va, vb)
    return (va + vb).tolist()


def subtract_vector(a: list[float], b: list[float]) -> list[float]:
    va, vb = validate_vector(a), validate_vector(b)
    validate_dimensions(va, vb)
    return (va - vb).tolist()


def scalar_multiply(a: list[float], escalar: float) -> list[float]:
    va = validate_vector(a)
    return (va * escalar).tolist()


def dot_product(a: list[float], b: list[float]) -> float:
    """Producto escalar (punto) [PDF §5: "cantidades × precios = ingresos"]."""
    va, vb = validate_vector(a), validate_vector(b)
    validate_dimensions(va, vb)
    return float(np.dot(va, vb))

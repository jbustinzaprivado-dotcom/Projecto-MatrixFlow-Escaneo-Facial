"""Álgebra lineal [PDF §11.3]: combinaciones lineales de vectores, para el "indicador
empresarial ponderado" de [PDF §5]. Por ahora solo entre vectores (mismo alcance que ya
tenía la página Combinaciones lineales del frontend, Fase 1)."""

from app.algorithms.vector_ops import validate_dimensions, validate_vector


def linear_combination(a: list[float], b: list[float], coeficiente_a: float, coeficiente_b: float) -> list[float]:
    """[PDF §11.3: linear_combination()] — c1·A + c2·B"""
    va, vb = validate_vector(a), validate_vector(b)
    validate_dimensions(va, vb)
    return (coeficiente_a * va + coeficiente_b * vb).tolist()

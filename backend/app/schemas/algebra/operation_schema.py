from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

TipoOperacion = Literal[
    "suma_vector",
    "resta_vector",
    "escalar_vector",
    "producto_escalar",
    "suma_matriz",
    "resta_matriz",
    "multiplicacion_matriz",
    "transpuesta_matriz",
    "escalar_matriz",
    "combinacion_lineal",
]

_REQUIERE_B = {
    "suma_vector",
    "resta_vector",
    "producto_escalar",
    "suma_matriz",
    "resta_matriz",
    "multiplicacion_matriz",
    "combinacion_lineal",
}
_REQUIERE_ESCALAR = {"escalar_vector", "escalar_matriz"}


class OperacionCreate(BaseModel):
    """Entrada de una operación. `escalar` es el multiplicador único de `escalar_vector` y
    `escalar_matriz`; `coeficiente_a`/`coeficiente_b` son los dos pesos de `combinacion_lineal`
    (c1·A + c2·B, [PDF §5]) — son campos distintos porque una combinación lineal siempre
    necesita dos coeficientes, no uno solo. Corrige una inconsistencia arrastrada desde la
    Fase 2, donde `combinacion_lineal` pedía un solo `escalar` sin decir para cuál vector era."""

    tipo: TipoOperacion
    vector_a_id: int | None = None
    vector_b_id: int | None = None
    matriz_a_id: int | None = None
    matriz_b_id: int | None = None
    escalar: float | None = None
    coeficiente_a: float | None = None
    coeficiente_b: float | None = None

    @model_validator(mode="after")
    def entradas_coherentes(self) -> "OperacionCreate":
        usa_matriz = self.tipo.endswith("matriz")
        principal = self.matriz_a_id if usa_matriz else self.vector_a_id
        if principal is None:
            objeto = "una matriz" if usa_matriz else "un vector"
            raise ValueError(f"La operación «{self.tipo}» necesita {objeto} de entrada (A).")
        secundario = self.matriz_b_id if usa_matriz else self.vector_b_id
        if self.tipo in _REQUIERE_B and secundario is None:
            objeto = "una matriz B" if usa_matriz else "un vector B"
            raise ValueError(f"La operación «{self.tipo}» necesita {objeto} además de la A.")
        if self.tipo in _REQUIERE_ESCALAR and self.escalar is None:
            raise ValueError(f"La operación «{self.tipo}» necesita un valor escalar.")
        if self.tipo == "combinacion_lineal" and (self.coeficiente_a is None or self.coeficiente_b is None):
            raise ValueError("La combinación lineal necesita «coeficiente_a» y «coeficiente_b».")
        return self


class OperacionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoOperacion
    entradas: str
    resultado: str | None
    estado: Literal["pendiente", "ok", "error"]
    mensaje: str
    creado_en: datetime

import re

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage

_PERIODO_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class MetaCreate(BaseModel):
    """[PDF §10: `targets`, RF-07] Meta de ventas por sucursal + producto + periodo — la
    pieza que faltaba para la resta matricial "ventas reales − metas" de [PDF §5]."""

    sucursal_id: int
    producto_id: int
    cantidad_meta: int
    periodo: str

    @field_validator("cantidad_meta")
    @classmethod
    def cantidad_positiva(cls, value: int) -> int:
        if value <= 0:
            raise ValidationMessage("La meta debe ser mayor a 0.")
        return value

    @field_validator("periodo")
    @classmethod
    def periodo_valido(cls, value: str) -> str:
        if not _PERIODO_RE.match(value):
            raise ValidationMessage('El periodo debe tener el formato "AAAA-MM", p. ej. "2026-09".')
        return value


class MetaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sucursal_id: int
    producto_id: int
    cantidad_meta: int
    periodo: str

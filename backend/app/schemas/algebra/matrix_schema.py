from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage


class MatrizCreate(BaseModel):
    nombre: str
    valores: list[list[float]]
    origen: str

    @field_validator("nombre", "origen")
    @classmethod
    def no_vacio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValidationMessage("El nombre y el origen no pueden estar vacíos.")
        return value

    @field_validator("valores")
    @classmethod
    def filas_parejas(cls, value: list[list[float]]) -> list[list[float]]:
        if not value or not value[0]:
            raise ValidationMessage("La matriz debe tener al menos una fila y una columna.")
        largo = len(value[0])
        if any(len(fila) != largo for fila in value):
            raise ValidationMessage("Todas las filas deben tener la misma cantidad de columnas.")
        return value


class MatrizOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    valores: list[list[float]]
    origen: str
    creado_en: datetime

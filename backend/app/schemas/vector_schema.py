from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage


class VectorCreate(BaseModel):
    nombre: str
    valores: list[float]
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
    def al_menos_un_valor(cls, value: list[float]) -> list[float]:
        if not value:
            raise ValidationMessage("El vector debe tener al menos un valor.")
        return value


class VectorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    valores: list[float]
    origen: str
    creado_en: datetime

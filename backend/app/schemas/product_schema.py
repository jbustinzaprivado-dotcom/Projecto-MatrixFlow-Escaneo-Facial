from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage


class ProductoCreate(BaseModel):
    nombre: str
    categoria: str
    precio: float

    @field_validator("nombre", "categoria")
    @classmethod
    def no_vacio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValidationMessage("El nombre y la categoría no pueden estar vacíos.")
        return value

    @field_validator("precio")
    @classmethod
    def precio_positivo(cls, value: float) -> float:
        if value <= 0:
            raise ValidationMessage("El precio debe ser mayor que cero.")
        return value


class ProductoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    categoria: str
    precio: float

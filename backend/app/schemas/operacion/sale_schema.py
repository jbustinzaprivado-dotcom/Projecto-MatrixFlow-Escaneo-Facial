from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage


class VentaCreate(BaseModel):
    sucursal_id: int
    producto_id: int
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, value: int) -> int:
        if value <= 0:
            raise ValidationMessage("La cantidad debe ser mayor que cero.")
        return value


class VentaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sucursal_id: int
    producto_id: int
    cantidad: int
    importe: float
    fecha: datetime

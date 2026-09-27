from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage


class InventarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sucursal_id: int
    producto_id: int
    existencias: int
    actualizado_en: datetime


class MovimientoCreate(BaseModel):
    """[PDF §10: `inventory_movements`, RF-06] Registra una entrada o salida de existencias
    para una sucursal + producto. Si no existe todavía una fila de `inventory` para esa
    combinación, se crea con 0 existencias antes de aplicar el movimiento."""

    sucursal_id: int
    producto_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, value: int) -> int:
        if value <= 0:
            raise ValidationMessage("La cantidad del movimiento debe ser mayor a 0.")
        return value


class MovimientoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inventario_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: int
    fecha: datetime

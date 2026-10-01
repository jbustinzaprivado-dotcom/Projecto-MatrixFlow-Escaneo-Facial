from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage


class SucursalCreate(BaseModel):
    nombre: str
    departamento: str
    distrito: str
    direccion: str

    @field_validator("nombre", "departamento", "distrito", "direccion")
    @classmethod
    def no_vacio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValidationMessage("Ningún campo de la sucursal puede estar vacío.")
        return value


class SucursalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    departamento: str
    distrito: str
    direccion: str

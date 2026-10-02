from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.errors import ValidationMessage

Rol = Literal["administrador", "analista", "consulta"]


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    dni: str
    rol: Rol
    sucursal_id: int

    @field_validator("nombre")
    @classmethod
    def nombre_valido(cls, value: str) -> str:
        value = value.strip()
        if not (2 <= len(value) <= 100):
            raise ValidationMessage("El nombre debe tener entre 2 y 100 caracteres.")
        return value

    @field_validator("email")
    @classmethod
    def email_valido(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or len(value) > 254:
            raise ValidationMessage("El correo no tiene un formato válido.")
        return value

    @field_validator("dni")
    @classmethod
    def dni_valido(cls, value: str) -> str:
        if not (value.isdigit() and len(value) == 8):
            raise ValidationMessage("El DNI debe tener exactamente 8 dígitos.")
        return value


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: str
    dni: str
    rol: Rol
    sucursal_id: int | None
    activo: bool
    creado_en: datetime
    rostros: int = 0


class RostroOut(BaseModel):
    usuario_id: int
    imagenes_guardadas: int


class VerificacionUsuario(BaseModel):
    nombre: str
    dni: str
    rol: Rol
    sede: str
    activo: bool
    creado_en: datetime


class VerificacionOut(BaseModel):
    """[Añadido D6, D80] 1:1, sin candidato cuando no coincide: nunca se dice quién era.
    Desde la Fase 6, `token` trae la sesión real cuando coincide (corrige D44)."""

    coincide: bool
    similitud: float
    usuario: VerificacionUsuario | None = None
    token: str | None = None
    # [Añadido, feedback del instructor] A nivel raíz, no dentro de VerificacionUsuario —
    # ese `creado_en` es la fecha de creación de la cuenta, un concepto distinto que no debe
    # mezclarse. Este es el momento real de ESTE ingreso, calculado en el servidor (nunca con
    # el reloj del navegador, mismo criterio que audit_logs/verificacion_intentos/D130).
    verificado_en: datetime | None = None


class CarnetOut(BaseModel):
    """[Añadido D8] solo datos + lo que el frontend convierte en QR (el DNI). Sin foto."""

    nombre: str
    dni: str
    rol: Rol
    sede: str
    activo: bool
    creado_en: datetime


class VerificacionIntentoOut(BaseModel):
    """[Añadido, Fase A2] historial de intentos de verificación, coincidan o no."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    dni: str
    usuario_id: int | None
    coincide: bool
    similitud: float | None
    creado_en: datetime

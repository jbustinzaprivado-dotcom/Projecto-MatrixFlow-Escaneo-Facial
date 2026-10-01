from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

from app.core.errors import ValidationMessage


class UbicacionIn(BaseModel):
    """[Añadido, corrige D9] Latitud/longitud que entrega `navigator.geolocation` en el
    navegador, cada ~60s mientras dura la sesión (`useUbicacionHeartbeat`, Layout.tsx)."""

    latitud: float
    longitud: float
    precision_m: float | None = None

    @field_validator("latitud")
    @classmethod
    def latitud_valida(cls, value: float) -> float:
        if not (-90 <= value <= 90):
            raise ValidationMessage("La latitud debe estar entre -90 y 90.")
        return value

    @field_validator("longitud")
    @classmethod
    def longitud_valida(cls, value: float) -> float:
        if not (-180 <= value <= 180):
            raise ValidationMessage("La longitud debe estar entre -180 y 180.")
        return value


class UbicacionActivaOut(BaseModel):
    """[Añadido, corrige D9] Una fila = la última posición conocida de un usuario con sesión
    activa (ventana D130), para el mapa en vivo de Auditoría (solo administrador)."""

    usuario_id: int
    usuario: str
    rol: Literal["administrador", "analista", "consulta"]
    sede: str
    latitud: float
    longitud: float
    precision_m: float | None
    actualizado_en: datetime

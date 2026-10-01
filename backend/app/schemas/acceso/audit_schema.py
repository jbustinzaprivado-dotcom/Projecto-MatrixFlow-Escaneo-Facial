from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AuditoriaEntradaOut(BaseModel):
    """[PDF §10: `audit_logs`] Una fila = un intento de inicio de sesión (D73)."""

    id: int
    usuario: str
    accion: str
    recurso: str
    resultado: Literal["ok", "error"]
    fecha: datetime
    sede: str


class ActividadDia(BaseModel):
    dia: str
    cantidad: int


class UsuarioActivo(BaseModel):
    usuario: str
    cantidad: int


class AuditoriaResumenOut(BaseModel):
    """[Añadido D5, D9] actividad de los últimos 7 días y ranking de más activos."""

    actividad_por_dia: list[ActividadDia]
    mas_activos: list[UsuarioActivo]
    total_7_dias: int

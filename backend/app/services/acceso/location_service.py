"""Ubicación en vivo del dispositivo durante la sesión [Añadido, corrige D9]. D9 (Fase 1)
descartó el GPS del navegador para la auditoría, por evitar pedir permisos y depender de un
servicio externo; el equipo, consultado de nuevo, decidió ahora sí trackear la posición real
del dispositivo mientras dura la sesión (D128) — no la sede fija de D9, que sigue intacta —,
con Leaflet + OpenStreetMap (sin API key) y permiso de navegador que, si se niega, no bloquea
nada (ver `useUbicacionHeartbeat` en el frontend). Una fila por usuario (upsert), no
historial: a diferencia de `audit_logs`/`verificacion_intentos`, esto es estado vivo de
"dónde está ahora", no un registro que deba sobrevivir para siempre."""

from datetime import timedelta

from sqlalchemy.orm import Session

from app.database.types import utcnow
from app.models import UbicacionUsuario
from app.repositories.acceso import location_repository

# D130: 2.5x el intervalo del heartbeat (60s, Layout.tsx) - tolera exactamente un latido
# perdido (hasta 60s de atraso) mas margen de red/jitter, sin que alguien realmente activo
# "parpadee" como desconectado entre dos latidos consecutivos.
VENTANA_ACTIVO_SEGUNDOS = 150


def _sede(ubicacion: UbicacionUsuario) -> str:
    if ubicacion.usuario.sucursal is not None:
        return ubicacion.usuario.sucursal.nombre
    return "—"


def reportar(
    db: Session, *, usuario_id: int, latitud: float, longitud: float, precision_m: float | None
) -> None:
    location_repository.upsert(
        db, usuario_id=usuario_id, latitud=latitud, longitud=longitud, precision_m=precision_m
    )


def listar_activas(db: Session) -> list[dict]:
    corte = utcnow() - timedelta(seconds=VENTANA_ACTIVO_SEGUNDOS)
    return [
        {
            "usuario_id": ubicacion.usuario_id,
            "usuario": ubicacion.usuario.nombre,
            "rol": ubicacion.usuario.rol.nombre,
            "sede": _sede(ubicacion),
            "latitud": float(ubicacion.latitud),
            "longitud": float(ubicacion.longitud),
            "precision_m": float(ubicacion.precision_m) if ubicacion.precision_m is not None else None,
            "actualizado_en": ubicacion.actualizado_en,
        }
        for ubicacion in location_repository.list_activas(db, corte)
    ]

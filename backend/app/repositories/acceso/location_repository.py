from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import UbicacionUsuario, Usuario


def upsert(
    db: Session, *, usuario_id: int, latitud: float, longitud: float, precision_m: float | None
) -> UbicacionUsuario:
    ubicacion = db.get(UbicacionUsuario, usuario_id)
    if ubicacion is None:
        ubicacion = UbicacionUsuario(usuario_id=usuario_id)
        db.add(ubicacion)
    ubicacion.latitud = latitud
    ubicacion.longitud = longitud
    ubicacion.precision_m = precision_m
    db.commit()
    db.refresh(ubicacion)
    return ubicacion


def list_activas(db: Session, desde: datetime) -> list[UbicacionUsuario]:
    return list(
        db.scalars(
            select(UbicacionUsuario)
            .options(
                selectinload(UbicacionUsuario.usuario).selectinload(Usuario.rol),
                selectinload(UbicacionUsuario.usuario).selectinload(Usuario.sucursal),
            )
            .where(UbicacionUsuario.actualizado_en >= desde)
            .order_by(UbicacionUsuario.actualizado_en.desc())
        )
    )

from datetime import datetime

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class UbicacionUsuario(Base):
    """Última posición conocida del dispositivo de cada usuario con sesión activa [Añadido,
    corrige D9] — fuera de las 19 tablas del documento, igual que `face_embeddings` y
    `verificacion_intentos`. D9 (Fase 1) fijó la "ubicación de auditoría" a la sede del perfil
    (`users.sucursal_id`) para evitar pedir permiso de GPS; el equipo, consultado de nuevo,
    decidió trackear la posición real del dispositivo mientras dura la sesión (D128). A
    diferencia de `audit_logs`/`verificacion_intentos` (historial permanente que nunca se
    borra), esta tabla guarda una sola fila por usuario — se sobrescribe en cada latido, cada
    ~60s (`useUbicacionHeartbeat` en el frontend) — y por eso usa `ondelete="CASCADE"`, al
    revés que las tablas de historial."""

    __tablename__ = "ubicaciones_usuario"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    latitud: Mapped[float] = mapped_column(Numeric(9, 6))
    longitud: Mapped[float] = mapped_column(Numeric(9, 6))
    precision_m: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    actualizado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow, onupdate=utcnow)

    usuario: Mapped["Usuario"] = relationship()

from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class VerificacionIntento(Base):
    """Historial de intentos de verificación [Añadido, Fase A2] — fuera de las 19 tablas del
    documento, igual que `face_embeddings`. Se guarda **cada** intento, coincida o no, con el
    DNI que se ingresó (decisión del equipo). Nunca se guarda quién fue el candidato cuando no
    coincide con el usuario buscado — eso ni siquiera aplica aquí, porque la comparación ya es
    1:1 contra el DNI ingresado (D6), no hay "otro candidato" que ocultar."""

    __tablename__ = "verificacion_intentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    dni: Mapped[str] = mapped_column(String(8))
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    coincide: Mapped[bool]
    similitud: Mapped[float | None] = mapped_column(Numeric(6, 4), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

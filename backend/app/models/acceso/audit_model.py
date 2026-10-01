from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class Auditoria(Base):
    """Auditoría [PDF §10: tabla `audit_logs`]. `sucursal_id` es la ubicación fija del login
    [Añadido D9]. Desde la Fase 6 (D73) esta tabla por fin se usa de verdad: cada intento de
    verificación (D70), coincida o no, escribe una fila aquí — es la fuente real de la
    Auditoría extendida (D5): actividad de 7 días, usuarios más activos y ubicación fija."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    accion: Mapped[str] = mapped_column(String(100))
    recurso: Mapped[str] = mapped_column(String(100))
    resultado: Mapped[str] = mapped_column(String(10))  # "ok" | "error"
    detalle: Mapped[str | None] = mapped_column(Text, nullable=True)
    sucursal_id: Mapped[int | None] = mapped_column(ForeignKey("branches.id"), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    usuario: Mapped["Usuario | None"] = relationship()
    sucursal: Mapped["Sucursal | None"] = relationship()

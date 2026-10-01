from datetime import datetime

from sqlalchemy import ForeignKey, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class Usuario(Base):
    """Usuarios del sistema [PDF §10: tabla `users`]. El `dni` y el `sucursal_id` son del
    ingreso por DNI + rostro y de la ubicación fija de auditoría [Añadido D6, D9] — el
    documento no los pide, pero la tabla ya existía y agregarlos ahora evita otra migración
    después. Sin autenticación por contraseña ni sesión: identificación biométrica solamente
    (Fase A), sin JWT ni RBAC todavía (eso seguiría siendo Fase 6, si se decide construirlo)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    dni: Mapped[str] = mapped_column(String(8), unique=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    sucursal_id: Mapped[int | None] = mapped_column(ForeignKey("branches.id"), nullable=True)
    activo: Mapped[bool] = mapped_column(default=True, server_default=true())
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    rol: Mapped["Rol"] = relationship()
    sucursal: Mapped["Sucursal | None"] = relationship()
    rostros: Mapped[list["RostroEmbedding"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )

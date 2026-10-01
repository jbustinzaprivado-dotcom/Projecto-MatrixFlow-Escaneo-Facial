from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class Inventario(Base):
    """Existencias [PDF §10: tabla `inventory`]."""

    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    existencias: Mapped[int]
    actualizado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    movimientos: Mapped[list["MovimientoInventario"]] = relationship(
        back_populates="inventario", cascade="all, delete-orphan"
    )


class MovimientoInventario(Base):
    """Movimientos [PDF §10: tabla `inventory_movements`]. Tabla creada en esta fase, sin
    endpoint todavía: el documento no asigna explícitamente esta pieza a ninguna fase futura
    (a diferencia de `operations`, que sí queda anotado para la Fase 4). Se retoma cuando el
    equipo decida construir el registro de movimientos."""

    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventario_id: Mapped[int] = mapped_column(ForeignKey("inventory.id", ondelete="CASCADE"))
    tipo: Mapped[str] = mapped_column(String(20))  # "entrada" | "salida"
    cantidad: Mapped[int]
    fecha: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    inventario: Mapped[Inventario] = relationship(back_populates="movimientos")

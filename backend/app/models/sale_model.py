from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow
from datetime import datetime


class Venta(Base):
    """Cabecera de ventas [PDF §10: tabla `sales`]."""

    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    fecha: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)
    total: Mapped[float] = mapped_column(Numeric(12, 2))

    detalles: Mapped[list["VentaDetalle"]] = relationship(
        back_populates="venta", cascade="all, delete-orphan"
    )


class VentaDetalle(Base):
    """Detalle de productos vendidos [PDF §10: tabla `sale_details`]."""

    __tablename__ = "sale_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    cantidad: Mapped[int]
    importe: Mapped[float] = mapped_column(Numeric(12, 2))

    venta: Mapped[Venta] = relationship(back_populates="detalles")

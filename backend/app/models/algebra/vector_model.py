from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class Vector(Base):
    """Vectores [PDF §10: tabla `vectors`]. Los valores viven aparte, uno por fila, en
    `vector_values` — así lo separa el propio documento en vez de guardar un arreglo."""

    __tablename__ = "vectors"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    origen: Mapped[str] = mapped_column(String(200))
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    valores: Mapped[list["VectorValor"]] = relationship(
        back_populates="vector", cascade="all, delete-orphan", order_by="VectorValor.posicion"
    )


class VectorValor(Base):
    """Valores de vectores [PDF §10: tabla `vector_values`]."""

    __tablename__ = "vector_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    vector_id: Mapped[int] = mapped_column(ForeignKey("vectors.id", ondelete="CASCADE"))
    posicion: Mapped[int]
    valor: Mapped[float] = mapped_column(Numeric(14, 4))

    vector: Mapped[Vector] = relationship(back_populates="valores")

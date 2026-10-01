from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class Matriz(Base):
    """Matrices [PDF §10: tabla `matrices`]. `filas`/`columnas` quedan guardadas aparte para
    no tener que contarlas cada vez; los valores viven en `matrix_values`."""

    __tablename__ = "matrices"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    origen: Mapped[str] = mapped_column(String(200))
    filas: Mapped[int]
    columnas: Mapped[int]
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    valores: Mapped[list["MatrizValor"]] = relationship(
        back_populates="matriz",
        cascade="all, delete-orphan",
        order_by="MatrizValor.fila, MatrizValor.columna",
    )


class MatrizValor(Base):
    """Valores matriciales [PDF §10: tabla `matrix_values`]."""

    __tablename__ = "matrix_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    matriz_id: Mapped[int] = mapped_column(ForeignKey("matrices.id", ondelete="CASCADE"))
    fila: Mapped[int]
    columna: Mapped[int]
    valor: Mapped[float] = mapped_column(Numeric(14, 4))

    matriz: Mapped[Matriz] = relationship(back_populates="valores")

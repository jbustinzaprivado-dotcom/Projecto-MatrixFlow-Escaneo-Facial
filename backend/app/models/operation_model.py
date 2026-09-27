from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class Operacion(Base):
    """Operaciones ejecutadas [PDF §10: tabla `operations`]. `estado` y `mensaje` no los
    nombra el documento, pero hacen falta para "guardar... estado de cada operación"; el
    resultado numérico vive aparte en `operation_results`, tal como lo separa la tabla."""

    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(30))
    estado: Mapped[str] = mapped_column(String(20))  # "pendiente" | "ok" | "error"
    mensaje: Mapped[str] = mapped_column(Text)
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    entradas: Mapped[list["OperacionEntrada"]] = relationship(
        back_populates="operacion", cascade="all, delete-orphan"
    )
    resultado: Mapped["OperacionResultado | None"] = relationship(
        back_populates="operacion", cascade="all, delete-orphan", uselist=False
    )


class OperacionEntrada(Base):
    """Entradas de operaciones [PDF §10: tabla `operation_inputs`]: una fila por cada vector,
    matriz o escalar que participa (A, B, o el escalar)."""

    __tablename__ = "operation_inputs"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation_id: Mapped[int] = mapped_column(ForeignKey("operations.id", ondelete="CASCADE"))
    rol: Mapped[str] = mapped_column(String(10))  # "a" | "b"
    tipo_entrada: Mapped[str] = mapped_column(String(10))  # "vector" | "matriz" | "escalar"
    referencia_id: Mapped[int | None]
    valor_escalar: Mapped[float | None] = mapped_column(Numeric(14, 4), nullable=True)

    operacion: Mapped[Operacion] = relationship(back_populates="entradas")


class OperacionResultado(Base):
    """Resultados [PDF §10: tabla `operation_results`]. `resultado` queda vacío mientras el
    motor NumPy de la Fase 4 no exista [PDF §11]."""

    __tablename__ = "operation_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation_id: Mapped[int] = mapped_column(
        ForeignKey("operations.id", ondelete="CASCADE"), unique=True
    )
    resultado: Mapped[str | None] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    operacion: Mapped[Operacion] = relationship(back_populates="resultado")

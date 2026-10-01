from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.database.types import UTCDateTime, utcnow


class RostroEmbedding(Base):
    """Vector facial (embedding) de un usuario [Añadido, Fase A — no está en las 19 tablas
    de PDF §10, es exclusivo del login biométrico]. Solo se guarda el vector (float32), nunca
    la foto: mismo principio de privacidad que Aurora Biometrics."""

    __tablename__ = "face_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    modelo: Mapped[str] = mapped_column(String(50))
    creado_en: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    usuario: Mapped["Usuario"] = relationship(back_populates="rostros")  # noqa: F821

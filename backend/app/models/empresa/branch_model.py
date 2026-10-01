from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Sucursal(Base):
    """Sedes de la empresa [PDF §10: tabla `branches`]."""

    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    nombre: Mapped[str] = mapped_column(String(100))
    departamento: Mapped[str] = mapped_column(String(100))
    distrito: Mapped[str] = mapped_column(String(100))
    direccion: Mapped[str] = mapped_column(String(200))

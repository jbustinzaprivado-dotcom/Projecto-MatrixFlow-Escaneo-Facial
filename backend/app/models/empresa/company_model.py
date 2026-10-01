from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Empresa(Base):
    """Información corporativa [PDF §10: tabla `companies`]."""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    razon_social: Mapped[str] = mapped_column(String(150))
    ruc: Mapped[str] = mapped_column(String(11), unique=True)
    rubro: Mapped[str] = mapped_column(String(150))

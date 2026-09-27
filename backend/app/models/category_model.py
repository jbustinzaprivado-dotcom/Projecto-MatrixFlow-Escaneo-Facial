from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Categoria(Base):
    """Categorías de productos [PDF §10: tabla `categories`]."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)

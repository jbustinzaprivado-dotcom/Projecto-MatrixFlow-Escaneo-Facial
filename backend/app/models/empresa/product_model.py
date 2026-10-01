from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Producto(Base):
    """Catálogo [PDF §10: tabla `products`]."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    precio: Mapped[float] = mapped_column(Numeric(10, 2))

    categoria: Mapped["Categoria"] = relationship()

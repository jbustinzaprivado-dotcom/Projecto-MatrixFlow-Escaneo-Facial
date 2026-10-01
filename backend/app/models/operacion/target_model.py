from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Meta(Base):
    """Metas empresariales [PDF §10: tabla `targets`; usadas en §5 para la resta matricial
    "ventas reales − metas"]. Tabla creada en esta fase, sin endpoint todavía — mismo caso
    que `inventory_movements`."""

    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    cantidad_meta: Mapped[int]
    periodo: Mapped[str] = mapped_column(String(20))  # p.ej. "2026-09"

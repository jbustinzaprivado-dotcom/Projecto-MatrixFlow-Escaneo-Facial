from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Vector, VectorValor


def list_all(db: Session) -> list[Vector]:
    return list(db.scalars(select(Vector).options(selectinload(Vector.valores)).order_by(Vector.id)))


def get(db: Session, vector_id: int) -> Vector | None:
    return db.scalar(
        select(Vector).options(selectinload(Vector.valores)).where(Vector.id == vector_id)
    )


def create(db: Session, *, nombre: str, origen: str, valores: list[float]) -> Vector:
    vector = Vector(nombre=nombre, origen=origen, creado_en=datetime.now(timezone.utc))
    db.add(vector)
    db.flush()
    db.add_all(VectorValor(vector_id=vector.id, posicion=i, valor=v) for i, v in enumerate(valores))
    db.commit()
    db.refresh(vector)
    return get(db, vector.id)  # type: ignore[return-value]

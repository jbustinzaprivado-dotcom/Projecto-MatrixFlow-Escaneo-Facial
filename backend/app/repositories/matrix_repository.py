from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Matriz, MatrizValor


def list_all(db: Session) -> list[Matriz]:
    return list(db.scalars(select(Matriz).options(selectinload(Matriz.valores)).order_by(Matriz.id)))


def get(db: Session, matriz_id: int) -> Matriz | None:
    return db.scalar(
        select(Matriz).options(selectinload(Matriz.valores)).where(Matriz.id == matriz_id)
    )


def create(db: Session, *, nombre: str, origen: str, valores: list[list[float]]) -> Matriz:
    matriz = Matriz(
        nombre=nombre,
        origen=origen,
        filas=len(valores),
        columnas=len(valores[0]) if valores else 0,
        creado_en=datetime.now(timezone.utc),
    )
    db.add(matriz)
    db.flush()
    db.add_all(
        MatrizValor(matriz_id=matriz.id, fila=i, columna=j, valor=valor)
        for i, fila in enumerate(valores)
        for j, valor in enumerate(fila)
    )
    db.commit()
    db.refresh(matriz)
    return get(db, matriz.id)  # type: ignore[return-value]

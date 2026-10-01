from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import RostroEmbedding


def list_by_usuario(db: Session, usuario_id: int, modelo: str) -> list[RostroEmbedding]:
    return list(
        db.scalars(
            select(RostroEmbedding).where(
                RostroEmbedding.usuario_id == usuario_id, RostroEmbedding.modelo == modelo
            )
        )
    )


def add(db: Session, *, usuario_id: int, embedding: bytes, modelo: str) -> RostroEmbedding:
    rostro = RostroEmbedding(usuario_id=usuario_id, embedding=embedding, modelo=modelo)
    db.add(rostro)
    db.commit()
    db.refresh(rostro)
    return rostro

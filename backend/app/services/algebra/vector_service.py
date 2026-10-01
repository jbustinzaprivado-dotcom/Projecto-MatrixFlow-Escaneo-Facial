from sqlalchemy.orm import Session

from app.repositories.algebra import vector_repository
from app.schemas.algebra.vector_schema import VectorCreate, VectorOut


def _to_out(vector) -> VectorOut:
    return VectorOut(
        id=vector.id,
        nombre=vector.nombre,
        valores=[float(v.valor) for v in vector.valores],
        origen=vector.origen,
        creado_en=vector.creado_en,
    )


def list_vectores(db: Session) -> list[VectorOut]:
    return [_to_out(v) for v in vector_repository.list_all(db)]


def create_vector(db: Session, data: VectorCreate) -> VectorOut:
    vector = vector_repository.create(db, nombre=data.nombre, origen=data.origen, valores=data.valores)
    return _to_out(vector)

from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireEscritura
from app.schemas.algebra.vector_schema import VectorCreate, VectorOut
from app.services.algebra import vector_service

router = APIRouter(prefix="/vectors", tags=["vectors"])


@router.get("", response_model=list[VectorOut])
def list_vectors(db: DbSession, _usuario: CurrentUser):
    return vector_service.list_vectores(db)


@router.post("", response_model=VectorOut, status_code=201)
def create_vector(data: VectorCreate, db: DbSession, _usuario: RequireEscritura):
    return vector_service.create_vector(db, data)

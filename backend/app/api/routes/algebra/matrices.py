from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireEscritura
from app.schemas.algebra.matrix_schema import MatrizCreate, MatrizOut
from app.services.algebra import matrix_service

router = APIRouter(prefix="/matrices", tags=["matrices"])


@router.get("", response_model=list[MatrizOut])
def list_matrices(db: DbSession, _usuario: CurrentUser):
    return matrix_service.list_matrices(db)


@router.post("", response_model=MatrizOut, status_code=201)
def create_matrix(data: MatrizCreate, db: DbSession, _usuario: RequireEscritura):
    return matrix_service.create_matriz(db, data)

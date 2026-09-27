from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireEscritura
from app.schemas.target_schema import MetaCreate, MetaOut
from app.services import target_service

router = APIRouter(prefix="/targets", tags=["targets"])


@router.get("", response_model=list[MetaOut])
def list_targets(db: DbSession, _usuario: CurrentUser):
    return target_service.list_metas(db)


@router.post("", response_model=MetaOut, status_code=201)
def create_target(data: MetaCreate, db: DbSession, _usuario: RequireEscritura):
    """[RF-07, Añadido en el repaso de fidelidad §16-21] Administrador o analista (§13)."""
    return target_service.create_meta(db, data)

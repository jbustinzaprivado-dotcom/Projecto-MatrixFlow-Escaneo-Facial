from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.core.errors import ApiException
from app.schemas.company_schema import EmpresaOut
from app.services import company_service

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=EmpresaOut)
def get_company(db: DbSession, _usuario: CurrentUser):
    empresa = company_service.get_empresa(db)
    if empresa is None:
        raise ApiException(404, "No hay una empresa registrada todavía.")
    return empresa

from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireEscritura
from app.schemas.sale_schema import VentaCreate, VentaOut
from app.services import sale_service

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("", response_model=list[VentaOut])
def list_sales(db: DbSession, _usuario: CurrentUser):
    return sale_service.list_ventas(db)


@router.post("", response_model=VentaOut, status_code=201)
def create_sale(data: VentaCreate, db: DbSession, _usuario: RequireEscritura):
    return sale_service.create_venta(db, data)

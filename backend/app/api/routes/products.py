from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireAdmin
from app.schemas.product_schema import ProductoCreate, ProductoOut
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductoOut])
def list_products(db: DbSession, _usuario: CurrentUser):
    return product_service.list_productos(db)


@router.post("", response_model=ProductoOut, status_code=201)
def create_product(data: ProductoCreate, db: DbSession, _usuario: RequireAdmin):
    """Solo administrador [corrige D71, repaso §16-21] — mismo criterio que sucursales."""
    return product_service.create_producto(db, data)

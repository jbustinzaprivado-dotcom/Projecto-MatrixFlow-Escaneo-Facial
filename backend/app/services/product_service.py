from sqlalchemy.orm import Session

from app.repositories import category_repository, product_repository
from app.schemas.product_schema import ProductoCreate, ProductoOut


def _to_out(producto) -> ProductoOut:
    return ProductoOut(
        id=producto.id,
        nombre=producto.nombre,
        categoria=producto.categoria.nombre,
        precio=float(producto.precio),
    )


def list_productos(db: Session) -> list[ProductoOut]:
    return [_to_out(p) for p in product_repository.list_all(db)]


def create_producto(db: Session, data: ProductoCreate) -> ProductoOut:
    categoria = category_repository.get_or_create(db, data.categoria)
    producto = product_repository.create(db, nombre=data.nombre, categoria_id=categoria.id, precio=data.precio)
    return ProductoOut(id=producto.id, nombre=producto.nombre, categoria=categoria.nombre, precio=float(producto.precio))

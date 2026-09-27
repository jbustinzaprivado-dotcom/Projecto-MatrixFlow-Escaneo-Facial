"""Se importan todos los modelos aquí para que Alembic los descubra a través de Base.metadata."""

from app.models.audit_model import Auditoria
from app.models.branch_model import Sucursal
from app.models.category_model import Categoria
from app.models.company_model import Empresa
from app.models.face_model import RostroEmbedding
from app.models.inventory_model import Inventario, MovimientoInventario
from app.models.matrix_model import Matriz, MatrizValor
from app.models.operation_model import Operacion, OperacionEntrada, OperacionResultado
from app.models.product_model import Producto
from app.models.role_model import Rol
from app.models.sale_model import Venta, VentaDetalle
from app.models.target_model import Meta
from app.models.user_model import Usuario
from app.models.vector_model import Vector, VectorValor
from app.models.verification_model import VerificacionIntento

__all__ = [
    "Auditoria",
    "Sucursal",
    "Categoria",
    "Empresa",
    "RostroEmbedding",
    "Inventario",
    "MovimientoInventario",
    "Matriz",
    "MatrizValor",
    "Operacion",
    "OperacionEntrada",
    "OperacionResultado",
    "Producto",
    "Rol",
    "Venta",
    "VentaDetalle",
    "Meta",
    "Usuario",
    "Vector",
    "VectorValor",
    "VerificacionIntento",
]

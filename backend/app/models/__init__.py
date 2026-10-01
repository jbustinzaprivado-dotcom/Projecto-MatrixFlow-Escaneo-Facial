"""Se importan todos los modelos aquí para que Alembic los descubra a través de Base.metadata."""

from app.models.acceso.audit_model import Auditoria
from app.models.empresa.branch_model import Sucursal
from app.models.empresa.category_model import Categoria
from app.models.empresa.company_model import Empresa
from app.models.biometria.face_model import RostroEmbedding
from app.models.operacion.inventory_model import Inventario, MovimientoInventario
from app.models.algebra.matrix_model import Matriz, MatrizValor
from app.models.algebra.operation_model import Operacion, OperacionEntrada, OperacionResultado
from app.models.empresa.product_model import Producto
from app.models.acceso.role_model import Rol
from app.models.operacion.sale_model import Venta, VentaDetalle
from app.models.operacion.target_model import Meta
from app.models.acceso.user_model import Usuario
from app.models.algebra.vector_model import Vector, VectorValor
from app.models.biometria.verification_model import VerificacionIntento

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

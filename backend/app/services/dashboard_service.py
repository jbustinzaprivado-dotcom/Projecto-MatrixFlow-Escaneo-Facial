"""Panel de indicadores [PDF §14, Fase 7]. Igual que report_service (Fase 5), agrega con
SQL en el servidor — el navegador ya no suma nada a partir de listas completas."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Operacion, Producto, Sucursal, Venta, VentaDetalle
from app.schemas.dashboard_schema import DashboardResumenOut


def build_resumen(db: Session) -> DashboardResumenOut:
    total_sedes = db.scalar(select(func.count(Sucursal.id))) or 0
    total_productos = db.scalar(select(func.count(Producto.id))) or 0
    total_ventas = db.scalar(select(func.coalesce(func.sum(Venta.total), 0))) or 0
    total_unidades = db.scalar(select(func.coalesce(func.sum(VentaDetalle.cantidad), 0))) or 0
    operaciones_ejecutadas = db.scalar(select(func.count(Operacion.id))) or 0

    return DashboardResumenOut(
        total_sedes=total_sedes,
        total_productos=total_productos,
        total_ventas=float(total_ventas),
        total_unidades=int(total_unidades),
        operaciones_ejecutadas=operaciones_ejecutadas,
    )

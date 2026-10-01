"""Panel de indicadores [PDF §14, Fase 7]. Igual que report_service (Fase 5), agrega con
SQL en el servidor — el navegador ya no suma nada a partir de listas completas."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Operacion, Producto, Sucursal, Venta, VentaDetalle
from app.schemas.reportes.dashboard_schema import DashboardResumenOut, TendenciaSemanaOut, VentasPorSedeOut


def _tendencia_semanal(db: Session) -> list[TendenciaSemanaOut]:
    """[Añadido] Serie temporal de ventas agrupada por semana (`date_trunc`), para graficar
    la tendencia real de las 16 semanas sembradas (D104) en vez de solo un total plano."""
    semana = func.date_trunc("week", Venta.fecha)
    filas = db.execute(
        select(semana.label("semana"), func.sum(Venta.total).label("total"))
        .group_by(semana)
        .order_by(semana)
    ).all()
    return [
        TendenciaSemanaOut(semana=fila.semana.strftime("%d %b"), total=float(fila.total))
        for fila in filas
    ]


def _ventas_por_sede(db: Session) -> list[VentasPorSedeOut]:
    """[Añadido] Total vendido por sucursal, para comparar las 5 sedes de un vistazo."""
    filas = db.execute(
        select(Sucursal.nombre.label("sede"), func.sum(Venta.total).label("total"))
        .join(Venta, Venta.sucursal_id == Sucursal.id)
        .group_by(Sucursal.nombre)
        .order_by(func.sum(Venta.total).desc())
    ).all()
    return [VentasPorSedeOut(sede=fila.sede, total=float(fila.total)) for fila in filas]


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
        tendencia_semanal=_tendencia_semanal(db),
        ventas_por_sede=_ventas_por_sede(db),
    )

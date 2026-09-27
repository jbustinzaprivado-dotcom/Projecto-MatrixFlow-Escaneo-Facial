from pydantic import BaseModel


class VentasPorSucursal(BaseModel):
    sucursal: str
    importe: float


class VentasPorProducto(BaseModel):
    producto: str
    cantidad: int


class ReporteOut(BaseModel):
    """Reporte básico de la Fase 2 [PDF §9.2]. El panel de indicadores más completo
    (gráficos, tendencias) es el entregable de la Fase 7, Analítica [PDF §7]."""

    ventas_por_sucursal: list[VentasPorSucursal]
    ventas_por_producto: list[VentasPorProducto]

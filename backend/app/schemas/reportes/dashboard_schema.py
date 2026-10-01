from pydantic import BaseModel


class TendenciaSemanaOut(BaseModel):
    """[Añadido] Un punto de la serie temporal de ventas, para el gráfico de tendencia."""

    semana: str
    total: float


class VentasPorSedeOut(BaseModel):
    """[Añadido] Un punto del comparativo de ventas por sucursal, para el gráfico de barras."""

    sede: str
    total: float


class DashboardResumenOut(BaseModel):
    """[PDF §14] Indicadores ejecutivos del panel principal."""

    total_sedes: int
    total_productos: int
    total_ventas: float
    total_unidades: int
    operaciones_ejecutadas: int
    tendencia_semanal: list[TendenciaSemanaOut]
    ventas_por_sede: list[VentasPorSedeOut]

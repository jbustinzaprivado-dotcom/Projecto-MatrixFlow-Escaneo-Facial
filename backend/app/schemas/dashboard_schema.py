from pydantic import BaseModel


class DashboardResumenOut(BaseModel):
    """[PDF §14] Indicadores ejecutivos del panel principal."""

    total_sedes: int
    total_productos: int
    total_ventas: float
    total_unidades: int
    operaciones_ejecutadas: int

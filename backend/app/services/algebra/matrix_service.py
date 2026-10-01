from sqlalchemy.orm import Session

from app.repositories.algebra import matrix_repository
from app.schemas.algebra.matrix_schema import MatrizCreate, MatrizOut


def _to_out(matriz) -> MatrizOut:
    grid = [[0.0] * matriz.columnas for _ in range(matriz.filas)]
    for valor in matriz.valores:
        grid[valor.fila][valor.columna] = float(valor.valor)
    return MatrizOut(
        id=matriz.id,
        nombre=matriz.nombre,
        valores=grid,
        origen=matriz.origen,
        creado_en=matriz.creado_en,
    )


def list_matrices(db: Session) -> list[MatrizOut]:
    return [_to_out(m) for m in matrix_repository.list_all(db)]


def create_matriz(db: Session, data: MatrizCreate) -> MatrizOut:
    matriz = matrix_repository.create(db, nombre=data.nombre, origen=data.origen, valores=data.valores)
    return _to_out(matriz)

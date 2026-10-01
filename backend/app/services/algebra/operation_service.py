"""Servicio de operaciones de la Fase 4: ya calcula de verdad con el módulo `algorithms/`
(Python + NumPy, [PDF §11]). Las reglas de validación de dimensiones ya no viven aquí —
viven en `algorithms/`, reutilizables y comprobables por separado, tal como pide el
documento — este servicio solo orquesta: busca los datos, llama al algoritmo, guarda.
"""

from sqlalchemy.orm import Session

from app.algorithms import linear_algebra, matrix_ops, vector_ops
from app.algorithms.errors import DimensionError
from app.core.errors import ApiException
from app.models import Matriz, Operacion, Vector
from app.repositories.algebra import matrix_repository, operation_repository, vector_repository
from app.schemas.algebra.operation_schema import OperacionCreate, OperacionOut


def _vector(db: Session, vector_id: int) -> Vector:
    vector = vector_repository.get(db, vector_id)
    if vector is None:
        raise ApiException(404, f"El vector {vector_id} no existe.")
    return vector


def _matriz(db: Session, matriz_id: int) -> Matriz:
    matriz = matrix_repository.get(db, matriz_id)
    if matriz is None:
        raise ApiException(404, f"La matriz {matriz_id} no existe.")
    return matriz


def _valores_vector(vector: Vector) -> list[float]:
    return [float(v.valor) for v in vector.valores]


def _valores_matriz(matriz: Matriz) -> list[list[float]]:
    grid = [[0.0] * matriz.columnas for _ in range(matriz.filas)]
    for valor in matriz.valores:
        grid[valor.fila][valor.columna] = float(valor.valor)
    return grid


def _formatear(valor: float | list[float] | list[list[float]]) -> str:
    def redondear(x: float) -> float:
        return round(x, 4)

    if isinstance(valor, list) and valor and isinstance(valor[0], list):
        return str([[redondear(x) for x in fila] for fila in valor])
    if isinstance(valor, list):
        return str([redondear(x) for x in valor])
    return str(redondear(valor))


def _ejecutar(db: Session, data: OperacionCreate) -> tuple[str, float | list, list[dict]]:
    """(descripción de las entradas, resultado calculado, filas para `operation_inputs`).
    Levanta `DimensionError` si las dimensiones no son compatibles [PDF: criterio CA-06]."""
    if data.tipo.endswith("matriz"):
        a = _matriz(db, data.matriz_a_id)  # type: ignore[arg-type]
        va = _valores_matriz(a)
        entradas = [{"rol": "a", "tipo_entrada": "matriz", "referencia_id": a.id}]

        if data.tipo == "transpuesta_matriz":
            return a.nombre, matrix_ops.transpose_matrix(va), entradas
        if data.tipo == "escalar_matriz":
            entradas.append({"rol": "b", "tipo_entrada": "escalar", "valor_escalar": data.escalar})
            return a.nombre, matrix_ops.scalar_multiply_matrix(va, data.escalar), entradas

        b = _matriz(db, data.matriz_b_id)  # type: ignore[arg-type]
        vb = _valores_matriz(b)
        entradas.append({"rol": "b", "tipo_entrada": "matriz", "referencia_id": b.id})
        descripcion = f"{a.nombre} · {b.nombre}"
        if data.tipo == "suma_matriz":
            return descripcion, matrix_ops.add_matrix(va, vb), entradas
        if data.tipo == "resta_matriz":
            return descripcion, matrix_ops.subtract_matrix(va, vb), entradas
        return descripcion, matrix_ops.multiply_matrix(va, vb), entradas  # multiplicacion_matriz

    a = _vector(db, data.vector_a_id)  # type: ignore[arg-type]
    va = _valores_vector(a)
    entradas = [{"rol": "a", "tipo_entrada": "vector", "referencia_id": a.id}]

    if data.tipo == "escalar_vector":
        entradas.append({"rol": "b", "tipo_entrada": "escalar", "valor_escalar": data.escalar})
        return a.nombre, vector_ops.scalar_multiply(va, data.escalar), entradas

    b = _vector(db, data.vector_b_id)  # type: ignore[arg-type]
    vb = _valores_vector(b)
    entradas.append({"rol": "b", "tipo_entrada": "vector", "referencia_id": b.id})
    descripcion = f"{a.nombre} · {b.nombre}"
    if data.tipo == "suma_vector":
        return descripcion, vector_ops.sum_vector(va, vb), entradas
    if data.tipo == "resta_vector":
        return descripcion, vector_ops.subtract_vector(va, vb), entradas
    if data.tipo == "producto_escalar":
        return descripcion, vector_ops.dot_product(va, vb), entradas
    # combinacion_lineal
    resultado = linear_algebra.linear_combination(va, vb, data.coeficiente_a, data.coeficiente_b)
    return descripcion, resultado, entradas


def _describir_entradas(db: Session, operacion: Operacion) -> str:
    """Reconstruye la descripción legible a partir de `operation_inputs`, para no duplicar
    el nombre del vector/matriz en dos tablas."""
    nombres = []
    for entrada in sorted(operacion.entradas, key=lambda e: e.rol):
        if entrada.tipo_entrada == "vector":
            v = vector_repository.get(db, entrada.referencia_id)
            nombres.append(v.nombre if v else f"Vector {entrada.referencia_id}")
        elif entrada.tipo_entrada == "matriz":
            m = matrix_repository.get(db, entrada.referencia_id)
            nombres.append(m.nombre if m else f"Matriz {entrada.referencia_id}")
        else:
            nombres.append(f"escalar {entrada.valor_escalar}")
    return " · ".join(nombres)


def _to_out(operacion: Operacion, entradas_desc: str) -> OperacionOut:
    return OperacionOut(
        id=operacion.id,
        tipo=operacion.tipo,
        entradas=entradas_desc,
        resultado=operacion.resultado.resultado if operacion.resultado else None,
        estado=operacion.estado,
        mensaje=operacion.mensaje,
        creado_en=operacion.creado_en,
    )


def create_operacion(db: Session, data: OperacionCreate) -> OperacionOut:
    try:
        entradas_desc, resultado, entradas_rows = _ejecutar(db, data)
    except DimensionError as error:
        # Las entradas ya se resolvieron (existen), solo fallaron las dimensiones: se guarda
        # igual en el historial con su motivo [PDF: "guardar... estado de cada operación"].
        entradas_desc, _, entradas_rows = _entradas_sin_calcular(db, data)
        operacion = operation_repository.create(
            db, tipo=data.tipo, estado="error", mensaje=str(error), entradas=entradas_rows
        )
        return _to_out(operacion, entradas_desc)

    operacion = operation_repository.create(
        db,
        tipo=data.tipo,
        estado="ok",
        mensaje="Cálculo realizado.",
        entradas=entradas_rows,
        resultado=_formatear(resultado),
    )
    return _to_out(operacion, entradas_desc)


def _entradas_sin_calcular(db: Session, data: OperacionCreate) -> tuple[str, None, list[dict]]:
    """Vuelve a armar la descripción y las filas de `operation_inputs` sin ejecutar el
    algoritmo, para el caso en que `_ejecutar` falló por dimensiones a mitad de camino."""
    if data.tipo.endswith("matriz"):
        a = _matriz(db, data.matriz_a_id)  # type: ignore[arg-type]
        entradas = [{"rol": "a", "tipo_entrada": "matriz", "referencia_id": a.id}]
        if data.matriz_b_id is None:
            return a.nombre, None, entradas
        b = _matriz(db, data.matriz_b_id)
        entradas.append({"rol": "b", "tipo_entrada": "matriz", "referencia_id": b.id})
        return f"{a.nombre} · {b.nombre}", None, entradas

    a = _vector(db, data.vector_a_id)  # type: ignore[arg-type]
    entradas = [{"rol": "a", "tipo_entrada": "vector", "referencia_id": a.id}]
    if data.vector_b_id is None:
        return a.nombre, None, entradas
    b = _vector(db, data.vector_b_id)
    entradas.append({"rol": "b", "tipo_entrada": "vector", "referencia_id": b.id})
    return f"{a.nombre} · {b.nombre}", None, entradas


def list_historial(db: Session) -> list[OperacionOut]:
    return [
        _to_out(operacion, _describir_entradas(db, operacion))
        for operacion in operation_repository.list_all(db)
    ]

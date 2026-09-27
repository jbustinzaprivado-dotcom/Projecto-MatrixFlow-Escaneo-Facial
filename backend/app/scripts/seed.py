"""Siembra datos de ejemplo ricos en información para poder visualizar bien cada módulo
[PDF §5]: ventas con variación temporal real (no todas en el mismo instante), metas,
vectores y matrices con sentido de negocio, historial con las 10 operaciones del motor
matemático ya ejecutadas, y actividad de auditoría repartida en varios días. Es idempotente:
si ya hay una empresa sembrada, no hace nada.

Uso: venv/bin/python -m app.scripts.seed
"""

import random
from datetime import datetime, timedelta, timezone

from app.database.connection import Base, SessionLocal, engine
from app.models import (
    Auditoria,
    Categoria,
    Empresa,
    Inventario,
    Meta,
    MovimientoInventario,
    Matriz,
    MatrizValor,
    Operacion,
    Producto,
    Rol,
    Sucursal,
    Usuario,
    Vector,
    VectorValor,
    Venta,
    VentaDetalle,
)
from app.schemas.operation_schema import OperacionCreate
from app.services import operation_service

random.seed(42)


def _now():
    return datetime.now(timezone.utc)


def seed() -> None:
    Base.metadata.create_all(engine)  # no-op si Alembic ya corrió; red de seguridad en dev
    db = SessionLocal()
    try:
        if db.query(Empresa).first() is not None:
            print("Ya hay datos sembrados; no se hace nada.")
            return

        empresa = Empresa(
            razon_social="MatrixFlow Enterprise S.A.C.",
            ruc="20601234567",
            rubro="Comercialización de equipos de cómputo",
        )
        db.add(empresa)
        db.flush()

        sedes_data = [
            ("Lima", "Lima", "San Isidro", "Av. Rivera Navarrete 501"),
            ("Arequipa", "Arequipa", "Yanahuara", "Calle Puente Grau 120"),
            ("Trujillo", "La Libertad", "Trujillo", "Jr. Pizarro 640"),
            ("Cusco", "Cusco", "Wanchaq", "Av. La Cultura 1300"),
            ("Piura", "Piura", "Piura", "Av. Grau 210"),
        ]
        sedes = [
            Sucursal(company_id=empresa.id, nombre=n, departamento=d, distrito=di, direccion=dir_)
            for n, d, di, dir_ in sedes_data
        ]
        db.add_all(sedes)
        db.flush()

        categorias = {
            nombre: Categoria(nombre=nombre) for nombre in ("Cómputo", "Periféricos", "Oficina")
        }
        db.add_all(categorias.values())
        db.flush()

        # Orden fijo: se reutiliza para alinear vectores/matrices por producto (misma
        # posición = mismo producto en todos lados).
        productos_data = [
            ("Laptop", "Cómputo", 3200),
            ("PC de escritorio", "Cómputo", 2400),
            ("Monitor", "Periféricos", 650),
            ("Teclado", "Periféricos", 120),
            ("Mouse", "Periféricos", 60),
            ("Impresora", "Oficina", 900),
        ]
        productos = [
            Producto(nombre=n, categoria_id=categorias[c].id, precio=p) for n, c, p in productos_data
        ]
        db.add_all(productos)
        db.flush()

        roles = {nombre: Rol(nombre=nombre) for nombre in ("administrador", "analista", "consulta")}
        db.add_all(roles.values())
        db.flush()

        usuarios_data = [
            ("Rosa Medina", "rosa.medina@matrixflow.demo", "71234567", "administrador", "Lima"),
            ("Jorge Salas", "jorge.salas@matrixflow.demo", "72345678", "analista", "Arequipa"),
            ("Lucía Fernández", "lucia.fernandez@matrixflow.demo", "73456789", "consulta", "Lima"),
        ]
        sede_por_nombre = {s.nombre: s for s in sedes}
        usuarios = [
            Usuario(
                nombre=nombre,
                email=email,
                dni=dni,
                rol_id=roles[rol].id,
                sucursal_id=sede_por_nombre[sede].id,
            )
            for nombre, email, dni, rol, sede in usuarios_data
        ]
        db.add_all(usuarios)
        db.flush()

        # --- Ventas: 16 semanas (~4 meses) por sede×producto, cantidades variables --------
        hoy = _now()
        semanas = 16
        totales_septiembre: dict[tuple[int, int], int] = {}  # (sede_id, producto_id) -> cantidad
        for si, sede in enumerate(sedes):
            for pi, producto in enumerate(productos):
                base = 5 + ((si + pi) % 4) * 3
                for semana in range(semanas):
                    fecha = hoy - timedelta(weeks=(semanas - 1 - semana))
                    variacion = random.randint(-3, 6)
                    cantidad = max(1, base + variacion + (semana % 3))
                    venta = Venta(
                        sucursal_id=sede.id, fecha=fecha, total=cantidad * float(producto.precio)
                    )
                    db.add(venta)
                    db.flush()
                    db.add(
                        VentaDetalle(
                            venta_id=venta.id,
                            producto_id=producto.id,
                            cantidad=cantidad,
                            importe=cantidad * float(producto.precio),
                        )
                    )
                    if fecha.year == 2026 and fecha.month == hoy.month:
                        clave = (sede.id, producto.id)
                        totales_septiembre[clave] = totales_septiembre.get(clave, 0) + cantidad

        # --- Inventario: existencias reales, construidas a partir de movimientos ---------
        for si, sede in enumerate(sedes):
            for pi, producto in enumerate(productos):
                objetivo = 20 + ((si + 1) * (pi + 1) * 3) % 60
                inventario = Inventario(
                    sucursal_id=sede.id, producto_id=producto.id, existencias=0, actualizado_en=hoy
                )
                db.add(inventario)
                db.flush()
                entrada = objetivo + 15
                db.add(
                    MovimientoInventario(
                        inventario_id=inventario.id,
                        tipo="entrada",
                        cantidad=entrada,
                        fecha=hoy - timedelta(weeks=3),
                    )
                )
                db.add(
                    MovimientoInventario(
                        inventario_id=inventario.id,
                        tipo="salida",
                        cantidad=15,
                        fecha=hoy - timedelta(weeks=1),
                    )
                )
                inventario.existencias = objetivo
        db.flush()

        # --- Metas: agosto y septiembre 2026, por sede×producto --------------------------
        metas_septiembre: dict[tuple[int, int], int] = {}
        for si, sede in enumerate(sedes):
            for pi, producto in enumerate(productos):
                venta_septiembre = totales_septiembre.get((sede.id, producto.id), 20)
                for periodo, factor in (("2026-08", 0.85), ("2026-09", 1.1 if (si + pi) % 2 else 0.9)):
                    cantidad_meta = max(5, round(venta_septiembre * factor))
                    db.add(
                        Meta(
                            sucursal_id=sede.id,
                            producto_id=producto.id,
                            cantidad_meta=cantidad_meta,
                            periodo=periodo,
                        )
                    )
                    if periodo == "2026-09":
                        metas_septiembre[(sede.id, producto.id)] = cantidad_meta
        db.flush()

        # --- Vectores: ventas y metas de septiembre por sede, alineados por producto ------
        def crear_vector(nombre: str, valores: list[float], origen: str) -> Vector:
            vector = Vector(nombre=nombre, origen=origen, creado_en=hoy)
            db.add(vector)
            db.flush()
            db.add_all(
                VectorValor(vector_id=vector.id, posicion=i, valor=v) for i, v in enumerate(valores)
            )
            return vector

        vectores_ventas: dict[str, Vector] = {}
        vectores_metas: dict[str, Vector] = {}
        for sede in sedes:
            ventas_valores = [totales_septiembre.get((sede.id, p.id), 0) for p in productos]
            metas_valores = [metas_septiembre.get((sede.id, p.id), 0) for p in productos]
            vectores_ventas[sede.nombre] = crear_vector(
                f"Ventas {sede.nombre} por producto",
                ventas_valores,
                f"Sucursal {sede.nombre}, septiembre 2026",
            )
            vectores_metas[sede.nombre] = crear_vector(
                f"Metas {sede.nombre} por producto", metas_valores, "Metas empresariales, septiembre 2026"
            )

        precios_vector = crear_vector(
            "Precios unitarios por producto",
            [float(p.precio) for p in productos],
            "Catálogo de productos [PDF §5: cantidades × precios = ingresos]",
        )

        vector_prueba_dimensiones = crear_vector(
            "Vector de prueba (3 valores)", [1, 2, 3], "Longitud distinta a propósito, para demostrar CA-06"
        )

        # --- Matrices: ventas, metas y precios --------------------------------------------
        def crear_matriz(nombre: str, filas: int, columnas: int, grid: list[list[float]], origen: str) -> Matriz:
            matriz = Matriz(nombre=nombre, origen=origen, filas=filas, columnas=columnas, creado_en=hoy)
            db.add(matriz)
            db.flush()
            db.add_all(
                MatrizValor(matriz_id=matriz.id, fila=f, columna=c, valor=grid[f][c])
                for f in range(filas)
                for c in range(columnas)
            )
            return matriz

        grid_ventas = [[float(totales_septiembre.get((s.id, p.id), 0)) for p in productos] for s in sedes]
        grid_metas = [[float(metas_septiembre.get((s.id, p.id), 0)) for p in productos] for s in sedes]
        grid_precios = [[float(p.precio)] for p in productos]

        matriz_ventas = crear_matriz(
            "Ventas por sucursal y producto",
            len(sedes),
            len(productos),
            grid_ventas,
            "Todas las sucursales, septiembre 2026 [PDF §5: Matriz]",
        )
        matriz_metas = crear_matriz(
            "Metas por sucursal y producto",
            len(sedes),
            len(productos),
            grid_metas,
            "Metas empresariales, septiembre 2026",
        )
        matriz_precios = crear_matriz(
            "Precios unitarios (columna)",
            len(productos),
            1,
            grid_precios,
            "Catálogo de productos, para multiplicación matricial",
        )

        db.commit()

        # --- Historial: las 10 operaciones del motor matemático, ya ejecutadas ------------
        # Se llama al servicio real (no se recalcula a mano) para que el resultado guardado
        # sea exactamente el que el sistema produciría — misma garantía que en producción.
        lima, arequipa = vectores_ventas["Lima"], vectores_ventas["Arequipa"]
        metas_lima = vectores_metas["Lima"]

        operaciones = [
            OperacionCreate(tipo="suma_vector", vector_a_id=lima.id, vector_b_id=metas_lima.id),
            OperacionCreate(tipo="resta_vector", vector_a_id=lima.id, vector_b_id=metas_lima.id),
            OperacionCreate(tipo="escalar_vector", vector_a_id=lima.id, escalar=1.15),
            OperacionCreate(
                tipo="producto_escalar", vector_a_id=lima.id, vector_b_id=precios_vector.id
            ),
            OperacionCreate(tipo="suma_matriz", matriz_a_id=matriz_ventas.id, matriz_b_id=matriz_metas.id),
            OperacionCreate(
                tipo="resta_matriz", matriz_a_id=matriz_ventas.id, matriz_b_id=matriz_metas.id
            ),
            OperacionCreate(
                tipo="multiplicacion_matriz", matriz_a_id=matriz_ventas.id, matriz_b_id=matriz_precios.id
            ),
            OperacionCreate(tipo="transpuesta_matriz", matriz_a_id=matriz_ventas.id),
            OperacionCreate(tipo="escalar_matriz", matriz_a_id=matriz_ventas.id, escalar=1.10),
            OperacionCreate(
                tipo="combinacion_lineal",
                vector_a_id=lima.id,
                vector_b_id=arequipa.id,
                coeficiente_a=0.6,
                coeficiente_b=0.4,
            ),
            # CA-06: dimensiones incompatibles a propósito, queda con estado "error".
            OperacionCreate(
                tipo="suma_vector", vector_a_id=lima.id, vector_b_id=vector_prueba_dimensiones.id
            ),
        ]
        for data in operaciones:
            operation_service.create_operacion(db, data)

        # Fila "pendiente" sintética: no hay ningún camino real que la produzca desde la
        # Fase 4 (el motor siempre resuelve a "ok" o "error"), pero Historial.tsx sabe
        # mostrar los 3 estados (D68) y conviene poder verlo en la demo sin depender de que
        # quede una fila vieja de alguna prueba manual.
        operacion_pendiente = Operacion(
            tipo="suma_vector",
            estado="pendiente",
            mensaje="Ejemplo sembrado para mostrar el estado pendiente en Historial.",
            creado_en=hoy - timedelta(days=2),
        )
        db.add(operacion_pendiente)

        # --- Auditoría: actividad repartida en los últimos 7 días -------------------------
        # Filas sintéticas insertadas directamente (no pasan por el login biométrico real):
        # son historial de demostración, no eventos de sesión reales.
        eventos_auditoria = []
        for dia_offset in range(7):
            fecha = hoy - timedelta(days=dia_offset, hours=random.randint(0, 8))
            for usuario in usuarios:
                if random.random() < 0.55:
                    continue
                resultado = "ok" if random.random() < 0.85 else "error"
                eventos_auditoria.append(
                    Auditoria(
                        usuario_id=usuario.id,
                        accion="Inicio de sesión",
                        recurso="Login biométrico (DNI + rostro)",
                        resultado=resultado,
                        detalle=None if resultado == "ok" else "Rostro no coincide con el registrado",
                        sucursal_id=usuario.sucursal_id,
                        creado_en=fecha,
                    )
                )
        db.add_all(eventos_auditoria)

        db.commit()
        print("Datos de ejemplo (ricos) sembrados correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

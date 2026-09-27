"""Fixtures de la Fase 8 [PDF §15]. Postgres real (`matrixflow_test`), no SQLite: el
documento fija PostgreSQL como motor (D3) y no hay razón para usar otra cosa solo en
pruebas — mismo criterio que ya se aplicó en la Fase 3 (D37: "reinició el servidor... los
datos siguieron ahí").

Cada prueba corre dentro de una transacción que se revierte al final (savepoint anidado):
las pruebas no se pisan entre sí y no hace falta recrear el esquema en cada una.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import crear_token
from app.database.connection import Base, get_db
from app.main import app
from app.models import Empresa, Rol, Sucursal, Usuario

TEST_DATABASE_URL = "postgresql+psycopg2://matrixflow:matrixflow_dev@localhost:5432/matrixflow_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def _esquema_de_prueba():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Generator[Session]:
    conexion = engine.connect()
    transaccion = conexion.begin()
    sesion = TestingSessionLocal(bind=conexion)
    try:
        yield sesion
    finally:
        sesion.close()
        transaccion.rollback()
        conexion.close()


@pytest.fixture
def client(db: Session) -> Generator[TestClient]:
    def _override_get_db():
        yield db

    app.dependency_overrides[get_db] = _override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def roles(db: Session) -> dict[str, Rol]:
    creados = {nombre: Rol(nombre=nombre) for nombre in ("administrador", "analista", "consulta")}
    db.add_all(creados.values())
    db.commit()
    return creados


@pytest.fixture
def sede(db: Session) -> Sucursal:
    empresa = Empresa(razon_social="Empresa de prueba", ruc="20000000001", rubro="Pruebas")
    db.add(empresa)
    db.commit()
    sucursal = Sucursal(
        company_id=empresa.id, nombre="Sede prueba", departamento="Lima", distrito="Lima", direccion="Calle 1"
    )
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    return sucursal


def crear_usuario(db: Session, *, rol: Rol, sede: Sucursal, dni: str, nombre: str = "Prueba") -> Usuario:
    usuario = Usuario(
        nombre=nombre, email=f"{dni}@test.com", dni=dni, rol_id=rol.id, sucursal_id=sede.id
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture
def usuarios(db: Session, roles: dict[str, Rol], sede: Sucursal) -> dict[str, Usuario]:
    return {
        nombre_rol: crear_usuario(db, rol=rol, sede=sede, dni=f"7{i}000000", nombre=nombre_rol.capitalize())
        for i, (nombre_rol, rol) in enumerate(roles.items())
    }


@pytest.fixture
def tokens(usuarios: dict[str, Usuario]) -> dict[str, str]:
    """Token real emitido por `core.security.crear_token` (D70): mismo mecanismo que usa
    `POST /verificacion` al coincidir, sin repetir el pipeline de OpenCV en cada prueba de
    RBAC — eso ya se verificó a mano con fotos reales en la Fase A (D45) y la Fase 6 (D78)."""
    return {rol: crear_token(u.id, rol) for rol, u in usuarios.items()}

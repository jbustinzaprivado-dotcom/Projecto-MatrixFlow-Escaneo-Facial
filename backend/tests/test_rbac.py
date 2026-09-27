"""RBAC de la Fase 6 (D71, D75): automatiza la misma matriz de 9 casos que se probó a
mano por curl en su momento (D78)."""

import pytest


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_sin_token_no_puede_leer(client):
    assert client.get("/api/v1/companies").status_code == 401


def test_token_invalido_no_puede_leer(client):
    assert client.get("/api/v1/companies", headers=auth("basura.no.valida")).status_code == 401


@pytest.mark.parametrize("rol", ["administrador", "analista", "consulta"])
def test_cualquier_rol_autenticado_puede_leer(client, tokens, rol):
    respuesta = client.get("/api/v1/companies", headers=auth(tokens[rol]))
    assert respuesta.status_code == 200


def test_consulta_no_puede_escribir(client, tokens):
    respuesta = client.post(
        "/api/v1/vectors",
        json={"nombre": "v", "valores": [1, 2, 3], "origen": "prueba"},
        headers=auth(tokens["consulta"]),
    )
    assert respuesta.status_code == 403


@pytest.mark.parametrize("rol", ["administrador", "analista"])
def test_administrador_y_analista_pueden_escribir(client, tokens, rol):
    respuesta = client.post(
        "/api/v1/vectors",
        json={"nombre": "v", "valores": [1, 2, 3], "origen": "prueba"},
        headers=auth(tokens[rol]),
    )
    assert respuesta.status_code == 201


def test_analista_no_puede_crear_usuarios(client, tokens, roles, sede):
    respuesta = client.post(
        "/api/v1/users",
        json={
            "nombre": "Nuevo",
            "email": "nuevo@test.com",
            "dni": "88000000",
            "rol": "consulta",
            "sucursal_id": sede.id,
        },
        headers=auth(tokens["analista"]),
    )
    assert respuesta.status_code == 403


def test_administrador_puede_crear_usuarios(client, tokens, roles, sede):
    respuesta = client.post(
        "/api/v1/users",
        json={
            "nombre": "Nuevo",
            "email": "nuevo@test.com",
            "dni": "88000000",
            "rol": "consulta",
            "sucursal_id": sede.id,
        },
        headers=auth(tokens["administrador"]),
    )
    assert respuesta.status_code == 201


def test_consulta_no_ve_historial_tecnico_de_verificaciones(client, tokens):
    assert client.get("/api/v1/verificacion", headers=auth(tokens["consulta"])).status_code == 403


def test_administrador_ve_historial_tecnico_de_verificaciones(client, tokens):
    assert client.get("/api/v1/verificacion", headers=auth(tokens["administrador"])).status_code == 200


# --- Corrección del repaso de fidelidad §16-21: sucursales/productos, solo administrador
# (D71 le daba escritura también a analista; §13 + CA-02 dicen que no) ---


def test_analista_no_puede_crear_sucursales(client, tokens):
    respuesta = client.post(
        "/api/v1/branches",
        json={"nombre": "Sede X", "departamento": "Lima", "distrito": "Lima", "direccion": "Calle X"},
        headers=auth(tokens["analista"]),
    )
    assert respuesta.status_code == 403


def test_administrador_puede_crear_sucursales(client, tokens):
    respuesta = client.post(
        "/api/v1/branches",
        json={"nombre": "Sede X", "departamento": "Lima", "distrito": "Lima", "direccion": "Calle X"},
        headers=auth(tokens["administrador"]),
    )
    assert respuesta.status_code == 201


def test_analista_no_puede_crear_productos(client, tokens):
    respuesta = client.post(
        "/api/v1/products",
        json={"nombre": "Producto X", "categoria": "Prueba", "precio": 10},
        headers=auth(tokens["analista"]),
    )
    assert respuesta.status_code == 403


def test_administrador_puede_crear_productos(client, tokens):
    respuesta = client.post(
        "/api/v1/products",
        json={"nombre": "Producto X", "categoria": "Prueba", "precio": 10},
        headers=auth(tokens["administrador"]),
    )
    assert respuesta.status_code == 201

"""CA-06 (dimensiones incompatibles) de punta a punta vía POST /operations real — D25, D29,
D40: un intento con dimensiones incompatibles no es un error HTTP, es una operación que
queda guardada con estado "error" en el historial."""


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def crear_vector(client, token, *, nombre, valores):
    respuesta = client.post(
        "/api/v1/vectors",
        json={"nombre": nombre, "valores": valores, "origen": "prueba"},
        headers=auth(token),
    )
    assert respuesta.status_code == 201
    return respuesta.json()["id"]


def test_suma_de_vectores_compatibles_da_resultado_real(client, tokens):
    token = tokens["analista"]
    id_a = crear_vector(client, token, nombre="A", valores=[1, 2, 3])
    id_b = crear_vector(client, token, nombre="B", valores=[4, 5, 6])

    respuesta = client.post(
        "/api/v1/operations",
        json={"tipo": "suma_vector", "vector_a_id": id_a, "vector_b_id": id_b},
        headers=auth(token),
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "ok"
    assert cuerpo["resultado"] == "[5.0, 7.0, 9.0]"


def test_suma_de_vectores_incompatibles_queda_como_error_ca06(client, tokens):
    token = tokens["analista"]
    id_a = crear_vector(client, token, nombre="A", valores=[1, 2, 3])
    id_b = crear_vector(client, token, nombre="B", valores=[1, 2])

    respuesta = client.post(
        "/api/v1/operations",
        json={"tipo": "suma_vector", "vector_a_id": id_a, "vector_b_id": id_b},
        headers=auth(token),
    )
    # No es un error HTTP (D29): la petición se acepta, la operación queda registrada.
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "error"
    assert cuerpo["resultado"] is None


def test_combinacion_lineal_con_dos_coeficientes(client, tokens):
    token = tokens["administrador"]
    id_a = crear_vector(client, token, nombre="A", valores=[1, 2, 3])
    id_b = crear_vector(client, token, nombre="B", valores=[4, 5, 6])

    respuesta = client.post(
        "/api/v1/operations",
        json={
            "tipo": "combinacion_lineal",
            "vector_a_id": id_a,
            "vector_b_id": id_b,
            "coeficiente_a": 2,
            "coeficiente_b": 3,
        },
        headers=auth(token),
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "ok"
    assert cuerpo["resultado"] == "[14.0, 19.0, 24.0]"

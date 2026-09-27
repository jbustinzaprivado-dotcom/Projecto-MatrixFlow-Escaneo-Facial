def test_infraestructura_de_pruebas_funciona(client, tokens):
    """Prueba mínima de que el TestClient real, la base de datos de prueba y los fixtures
    de usuarios/roles/tokens funcionan antes de escribir el resto de la suite. El fixture
    `tokens` (vía `usuarios` -> `sede`) ya crea una empresa real, así que se espera 200."""
    respuesta = client.get(
        "/api/v1/companies", headers={"Authorization": f"Bearer {tokens['administrador']}"}
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["razon_social"] == "Empresa de prueba"


def test_sin_token_da_401(client):
    respuesta = client.get("/api/v1/companies")
    assert respuesta.status_code == 401

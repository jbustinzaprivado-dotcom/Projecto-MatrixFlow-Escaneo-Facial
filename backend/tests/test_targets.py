"""RF-07 (repaso de fidelidad §16-21): registrar metas — la pieza que faltaba para la
resta matricial "ventas reales − metas" de [PDF §5]."""


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_consulta_no_puede_registrar_meta(client, tokens, sede):
    respuesta = client.post(
        "/api/v1/targets",
        json={"sucursal_id": sede.id, "producto_id": 1, "cantidad_meta": 100, "periodo": "2026-09"},
        headers=auth(tokens["consulta"]),
    )
    assert respuesta.status_code == 403


def test_analista_registra_y_lista_una_meta(client, tokens, sede):
    token = tokens["analista"]
    producto = client.post(
        "/api/v1/products",
        json={"nombre": "Producto meta", "categoria": "Prueba", "precio": 10},
        headers=auth(tokens["administrador"]),
    ).json()

    creada = client.post(
        "/api/v1/targets",
        json={
            "sucursal_id": sede.id,
            "producto_id": producto["id"],
            "cantidad_meta": 150,
            "periodo": "2026-09",
        },
        headers=auth(token),
    )
    assert creada.status_code == 201
    assert creada.json()["cantidad_meta"] == 150

    listadas = client.get("/api/v1/targets", headers=auth(token)).json()
    assert any(m["id"] == creada.json()["id"] for m in listadas)


def test_periodo_con_formato_invalido_da_422(client, tokens, sede):
    respuesta = client.post(
        "/api/v1/targets",
        json={"sucursal_id": sede.id, "producto_id": 1, "cantidad_meta": 100, "periodo": "septiembre-2026"},
        headers=auth(tokens["administrador"]),
    )
    assert respuesta.status_code == 422

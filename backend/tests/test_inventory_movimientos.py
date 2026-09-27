"""RF-06 (repaso de fidelidad §16-21): registrar movimientos reales de inventario."""


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_consulta_no_puede_registrar_movimiento(client, tokens):
    respuesta = client.post(
        "/api/v1/inventory/movimientos",
        json={"sucursal_id": 1, "producto_id": 1, "tipo": "entrada", "cantidad": 5},
        headers=auth(tokens["consulta"]),
    )
    assert respuesta.status_code == 403


def test_entrada_crea_inventario_en_cero_y_lo_incrementa(client, tokens, sede):
    token = tokens["analista"]
    producto = client.post(
        "/api/v1/products",
        json={"nombre": "Producto inventario", "categoria": "Prueba", "precio": 10},
        headers=auth(tokens["administrador"]),
    ).json()

    respuesta = client.post(
        "/api/v1/inventory/movimientos",
        json={"sucursal_id": sede.id, "producto_id": producto["id"], "tipo": "entrada", "cantidad": 20},
        headers=auth(token),
    )
    assert respuesta.status_code == 201

    inventario = client.get("/api/v1/inventory", headers=auth(token)).json()
    fila = next(i for i in inventario if i["producto_id"] == producto["id"])
    assert fila["existencias"] == 20


def test_salida_sin_existencias_suficientes_da_422(client, tokens, sede):
    token = tokens["analista"]
    producto = client.post(
        "/api/v1/products",
        json={"nombre": "Producto sin stock", "categoria": "Prueba", "precio": 10},
        headers=auth(tokens["administrador"]),
    ).json()

    respuesta = client.post(
        "/api/v1/inventory/movimientos",
        json={"sucursal_id": sede.id, "producto_id": producto["id"], "tipo": "salida", "cantidad": 1},
        headers=auth(token),
    )
    assert respuesta.status_code == 422


def test_entrada_y_salida_dejan_el_saldo_correcto(client, tokens, sede):
    token = tokens["analista"]
    producto = client.post(
        "/api/v1/products",
        json={"nombre": "Producto saldo", "categoria": "Prueba", "precio": 10},
        headers=auth(tokens["administrador"]),
    ).json()

    client.post(
        "/api/v1/inventory/movimientos",
        json={"sucursal_id": sede.id, "producto_id": producto["id"], "tipo": "entrada", "cantidad": 30},
        headers=auth(token),
    )
    client.post(
        "/api/v1/inventory/movimientos",
        json={"sucursal_id": sede.id, "producto_id": producto["id"], "tipo": "salida", "cantidad": 12},
        headers=auth(token),
    )

    inventario = client.get("/api/v1/inventory", headers=auth(token)).json()
    fila = next(i for i in inventario if i["producto_id"] == producto["id"])
    assert fila["existencias"] == 18

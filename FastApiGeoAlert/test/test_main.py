from fastapi.testclient import TestClient
from FastApiGeoAlert.main import app

client = TestClient(app)

def test_crear_y_obtener_alerta():
    data = {
        "titulo": "Prueba",
        "descripcion": "Test",
        "latitud": 10.0,
        "longitud": 20.0,
        "categoria": "prueba",
        "nivel_alerta": 2
    }
    # Crear alerta
    response = client.post("/alertas", json=data)
    assert response.status_code == 201  # Usualmente creación retorna 201
    alerta = response.json()
    for key in data:
        assert alerta[key] == data[key]

    # Obtener alerta por ID
    response = client.get(f"/alertas/{alerta['id']}")
    assert response.status_code == 200
    alerta_obtenida = response.json()
    assert alerta_obtenida["id"] == alerta["id"]
    for key in data:
        assert alerta_obtenida[key] == data[key]

def test_obtener_imagenes_sentinel():
    # Ejemplo de bbox y fecha (ajusta según tu área de interés)
    params = {
        "bbox": "-58,-34,-57,-33",
        "fecha": "2024-07-01"
    }
    response = client.get("/sentinel/imagenes", params=params)
    # El endpoint externo puede variar, así que solo verifica que responde
    assert response.status_code in [200, 502]
    # Si es 200, debe devolver un JSON
    if response.status_code == 200:
        assert isinstance(response.json(), dict) or isinstance(response.json(), list)

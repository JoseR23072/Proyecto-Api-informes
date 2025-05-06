# tests/test_crear_batida_unitario.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.batida.BatidaCreateDto import BatidaCreateDto
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService  # IMPORTANTE: el mismo objeto que usas en Depends

client = TestClient(app)

class FakeService:
    async def crear_batida(self, dto: BatidaCreateDto) -> BatidaResponseDto:
        return BatidaResponseDto(
            id_batida=999,
            nombre=dto.nombre,
            latitud=dto.latitud,
            longitud=dto.longitud,
            zona={
                
            },          # rellena tu ZonaDto de prueba
            voluntarios=[],
            estado=dto.estado,
            fecha_evento=dto.fecha_evento,
            descripcion=dto.descripcion
        )

@pytest.fixture(autouse=True)
def override_service():
    app.dependency_overrides[BatidaService] = lambda: FakeService()
    yield
    app.dependency_overrides.clear()

def test_crear_batida_unitario_exito():
    payload = {
        "nombre": "Unidad Mock",
        "latitud": 10.5,
        "longitud": -20.5,
        "id_zona": 1,
        "fecha_evento": "2025-07-01",
        "descripcion": "Prueba unitaria",
        "estado": True
    }

    response = client.post("/riverspain/batida", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id_batida"] == 999
    assert data["nombre"] == payload["nombre"]
    assert data["estado"] is True

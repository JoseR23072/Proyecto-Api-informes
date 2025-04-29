from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class BatidaUpdateDto(BaseModel):
    id_batida: int = Field(..., gt=0, description="ID de la batida a modificar")
    nombre: Optional[str] = Field(None, min_length=1, description="Nuevo nombre de la batida")
    latitud: Optional[float] = Field(None, ge=-90, le=90, description="Nueva latitud")
    longitud: Optional[float] = Field(None, ge=-180, le=180, description="Nueva longitud")
    id_zona: Optional[int] = Field(None, gt=0, description="Nuevo ID de la zona asociada")
    fecha_evento: Optional[date] = Field(None, description="Nueva fecha del evento")
    descripcion: Optional[str] = Field(None, min_length=1, description="Nueva descripción")
    voluntarios: Optional[str] = Field(
        None,
        description="Lista de Codigos de voluntarios asignados a la batida"
    )
    estado: Optional[bool] = Field(None, description="Nuevo estado de la batida (activa/inactiva)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id_batida": 1,
                    "nombre": "Nombre de la batida actualizada",
                    "descripcion": "Nueva descripción de la batida",
                    "latitud": 40.1234,
                    "longitud": -3.5678,
                    "id_zona": 3,
                    "fecha_evento": "2025-05-10",
                    "voluntarios": '["MI123455","MI9328234"]',
                    "estado": True
                }
            ]
        }
    }

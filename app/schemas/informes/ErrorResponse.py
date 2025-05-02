from pydantic import BaseModel, Field
from typing import List, Dict, Any


class QueryValidationErrorBatidaResponse(BaseModel):
    code: int = Field(
        42210,
        description="Código específico para errores de validación de path parameters en delete de batida"
    )
    message: str = Field(
        "Error de validación de parámetros de ruta.",
        description="Descripción general del error de validación en los parámetros de la ruta"
    )
    details: List[Dict[str, Any]] = Field(
        ...,
        description="Lista de detalles con la ubicación, mensaje y tipo de cada error de validación"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 42210,
                    "message": "Error de validación de query parameters.",
                    "details": [
                        {
                            "loc": ["query", "id_batida"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer"
                        },
                        {
                            "loc": ["query", "formato"],
                            "msg": "unexpected value; permitted: 'pdf', 'excel'",
                            "type": "value_error.const"
                        }
                    ]
                }
            ]
        }
    }

class QueryValidationErrorZonaResponse(QueryValidationErrorBatidaResponse):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 42210,
                    "message": "Error de validación de query parameters.",
                    "details": [
                        {
                            "loc": ["query", "id_zona"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer"
                        },
                        {
                            "loc": ["query", "formato"],
                            "msg": "unexpected value; permitted: 'pdf', 'excel'",
                            "type": "value_error.const"
                        }
                    ]
                }
            ]
        }
    }
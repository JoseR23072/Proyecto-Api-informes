from pydantic import BaseModel, Field
from typing import Optional
import datetime
from typing import List, Dict, Any


class SchedulerTimeDto(BaseModel):
    hora: int = Field(..., ge=0, le=23, description="Hora en formato 0-23")
    minuto: int = Field(..., ge=0, le=59, description="Minuto en formato 0-59")

class SchedulerTimeResponseDto(BaseModel):
    hora: int = Field(..., description="Hora programada")
    minuto: int = Field(..., description="Minuto programado")
    proxima_tarea: Optional[datetime.datetime] = Field(None, description="Próxima ejecución programada")

class ValidationErrorReprogramarTareaResponse(BaseModel):
    code: int = Field(
        42220,
        description="Código específico para errores de validación de reprogramación de tarea"
    )
    message: str = Field(
        "Error de validación en los parámetros de la petición.",
        description="Mensaje general del error de validación"
    )
    details: List[Dict[str, Any]] = Field(
        ...,
        description="Lista de objetos con `loc`, `msg` y `type` para cada error de campo"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 42220,
                    "message": "Error de validación en los parámetros de la petición.",
                    "details": [
                        {
                            "loc": ["body", "hora"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer"
                        },
                        {
                            "loc": ["body", "minuto"],
                            "msg": "ensure this value is less than or equal to 59",
                            "type": "value_error.number.not_le"
                        }
                    ]
                }
            ]
        }
    }


class EnvioRecordatorioResponseDto(BaseModel):
    code: int = Field(
        20000,
        description="Código específico que indica envío exitoso de recordatorio"
    )
    message: str = Field(
        ...,
        description="Mensaje confirmando el envío del recordatorio"
    )
    

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 20000,
                    "message": "Recordatorio enviado para batida 42",
                }
            ]
        }
    }


class BatidaNotFoundResponse(BaseModel):
    code: int = Field(40410, description="Código específico para batida no encontrada")
    message: str = Field(..., description="Mensaje explicando que la batida no existe")
    details: Optional[str] = Field(None, description="Detalles adicionales del error")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40410,
                    "message": "La batida con ID 999 no existe.",
                    "details": "Imposible enviar un recordatoria a una batida inexistente"
                }
            ]
        }
    }


class PathParamUtilitiesValidationErrorResponse(BaseModel):
    code: int = Field(
        42210,
        description="Código específico para errores de validación de path parameters en busqueda de batida"
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
                    "message": "Error de validación de parámetros de ruta.",
                    "details": [
                        {
                            "loc": ["path", "id_batida"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer"
                        }
                    ]
                }
            ]
        }
    }

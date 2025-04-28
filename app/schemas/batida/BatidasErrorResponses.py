from pydantic import BaseModel, Field
from typing import Optional

class ValidationErrorResponse(BaseModel):
    code: int = Field(40000, description="Código específico para errores de validación")
    message: str = Field(..., description="Mensaje explicativo del error de validación")
    details: Optional[str] = Field(None, description="Detalles adicionales del error (opcional)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40000,
                    "message": "Los datos enviados no cumplen con el formato requerido.",
                    "details": "El campo 'nombre' es obligatorio."
                }
            ]
        }
    }

class InternalServerErrorResponse(BaseModel):
    code: int = Field(50000, description="Código específico para errores internos del servidor")
    message: str = Field(..., description="Mensaje de error interno del servidor")
    details: Optional[str] = Field(None, description="Información adicional para soporte técnico (opcional)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 50000,
                    "message": "Error interno inesperado.",
                    "details": "Error en la base de datos."
                }
            ]
        }
    }

class NotFoundErrorResponse(BaseModel):
    code: int = Field(40400, description="Código específico para recurso no encontrado")
    message: str = Field(..., description="Mensaje explicando que el recurso solicitado no fue encontrado")
    details: Optional[str] = Field(None, description="Detalles adicionales sobre el error")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40400,
                    "message": "Recurso solicitado no encontrado.",
                    "details": "La ruta '/batidas/999' no existe."
                }
            ]
        }
    }

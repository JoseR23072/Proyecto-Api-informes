from pydantic import BaseModel, Field
from typing import List, Dict, Any,Optional
class ValidationErrorResponse(BaseModel):
    code: int = Field(40000, description="Código específico para errores de validación")
    message: str = Field(..., description="Mensaje explicativo del error de validación")
    details: Optional[str] = Field(None, description="Detalles adicionales del error (opcional)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40000,
                    "message": "Validación de negocio fallida.",
                    "details": "La zona con ID 999 no existe."
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
                    "message": "La batida con ID 999 no fue encontrada.",
                    "details": "No existe ninguna batida con ese identificador en la base de datos."
                }
            ]
        }
    }

class NotBatidasFoundResponse(BaseModel):
    code: int = Field(40401, description="Código específico indicando que no existen batidas registradas")
    message: str = Field(..., description="Mensaje indicando que no se encontraron batidas")
    details: Optional[str] = Field(None, description="Detalles adicionales sobre la ausencia de batidas (opcional)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40401,
                    "message": "No se encontraron batidas registradas.",
                    "details": "Actualmente no hay ninguna batida en el sistema."
                }
            ]
        }
    }

class UnprocessableEntityResponse(BaseModel):
    code: int = Field(42200, description="Código de error específico para errores de validación de entrada")
    message: str = Field("Error de validación en la solicitud.", description="Descripción del error")
    details: List[Dict[str, Any]] = Field(..., description="Detalles de los errores de validación")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 42200,
                    "message": "Error de validación en la solicitud.",
                    "details": [
                        {
                            "loc": ["body", "nombre"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                }
            ]
        }
    }

class UnprocessableEntityResponseGet(BaseModel):
    code: int = Field(42200, description="Código de error específico para errores de validación de entrada")
    message: str = Field("Error de validación en la solicitud.", description="Descripción del error")
    details: List[Dict[str, Any]] = Field(..., description="Detalles de los errores de validación")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 42200,
                    "message": "Error de validación en la solicitud.",
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

class VoluntarioDuplicadoResponse(BaseModel):
    code: int = Field(40010, description="Código específico para voluntario duplicado")
    message: str = Field(..., description="Mensaje indicando que el voluntario ya está apuntado")
    details: Optional[str] = Field(None, description="Detalles adicionales (ID o contexto)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 40010,
                    "message": "El voluntario V123 ya está apuntado a la batida.",
                    "details": "Código de voluntario duplicado en la lista."
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
                    "message": "La batida con ID 5 no existe.",
                    "details": "Imposible apuntar voluntario a batida inexistente."
                }
            ]
        }
    }

class PathParamValidationErrorResponse(BaseModel):
    code: int = Field(42210, description="Código específico para errores de validación de path parameters")
    message: str = Field("Error de validación de parámetros de ruta.", description="Descripción general del error")
    details: List[Dict[str, Any]] = Field(..., description="Detalles de la validación de parámetros")

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
                        },
                        {
                            "loc": ["path", "codigo_voluntario"],
                            "msg": "string does not match regex \"^V[0-9]+$\"",
                            "type": "value_error.str.regex"
                        }
                    ]
                }
            ]
        }
    }

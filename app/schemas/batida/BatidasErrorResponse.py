from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"detail": "El ID de zona no existe"}
            ]
        }
    }
import httpx
from pydantic import BaseModel, EmailStr
from datetime import date
class VoluntarioDto(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: EmailStr
    dni: str
    numerovoluntario: str
    rol: str | None = None
    fechacreacion: date | None = None

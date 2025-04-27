import httpx
from pydantic import BaseModel, EmailStr

class VoluntarioDto(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: EmailStr
    dni: str
    numerovoluntario: str
    rol: str | None = None

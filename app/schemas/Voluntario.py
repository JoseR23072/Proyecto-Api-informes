import httpx
from pydantic import BaseModel, EmailStr

class VoluntarioDto(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    dni: str
    numeroVoluntario: str

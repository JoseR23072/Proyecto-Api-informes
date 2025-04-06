from fastapi import APIRouter, Depends
# from app.schemas.Voluntario import VoluntarioCreate, VoluntarioRead
from app.schemas.Voluntario import VoluntarioDto
from app.services.InformeService import create_voluntario

router = APIRouter()

@router.post("/prueba", response_model=VoluntarioDto)
def crear_voluntario(voluntario: VoluntarioDto):
    return create_voluntario(voluntario)

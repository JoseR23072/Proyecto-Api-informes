from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
# from app.schemas.Voluntario import VoluntarioCreate, VoluntarioRead
from app.schemas.Voluntario import VoluntarioDto
from app.services.InformeService import create_voluntario
from app.utils import recordatorio
router = APIRouter()

@router.post("/prueba", response_model=VoluntarioDto)
def crear_voluntario(voluntario: VoluntarioDto):
    return create_voluntario(voluntario)

@router.get("/recordatorio")
def obtener_recordatorio():
    # Datos de prueba
    nombre_voluntario = "Laura Martínez"
    nombre_batida = "Batida Playa del Faro"
    fecha = "2025-04-10"
    ciudad = "Málaga"
    latitud = 36.7213
    longitud = -4.4214

    path_pdf = recordatorio.generar_pdf_recordatorio(
        nombre_voluntario=nombre_voluntario,
        nombre_batida=nombre_batida,
        fecha=fecha,
        latitud=latitud,
        longitud=longitud,
        ciudad=ciudad
    )

    return FileResponse(
        path=path_pdf,
        media_type='application/pdf',
        filename=path_pdf.split("/")[-1]
    )
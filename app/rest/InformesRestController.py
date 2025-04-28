from fastapi import APIRouter, Depends,BackgroundTasks
from fastapi.responses import FileResponse
# from app.schemas.Voluntario import VoluntarioCreate, VoluntarioRead
from schemas.Voluntario import VoluntarioDto
from utils import recordatorio
import os

def eliminar_archivo(path: str):
    if os.path.exists(path):
        print("Se va a eliminar ela rchivo")
        os.remove(path)
        print(f"archivo eliminado correctamente: {path}")

router = APIRouter()

@router.post("/informes/{zona_id}", response_model=VoluntarioDto)
def generar_informe(zona_id: int):
    
    return None

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
    # Programamos la eliminación del archivo una vez se termine de enviar
    #BackgroundTasks.add_task(eliminar_archivo,path_pdf)
    return FileResponse(
        path=path_pdf,
        media_type='application/pdf',
        filename=path_pdf.split("/")[-1]
    )
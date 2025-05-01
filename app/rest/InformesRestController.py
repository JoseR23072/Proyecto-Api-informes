from fastapi import APIRouter, Depends,BackgroundTasks,HTTPException
from fastapi.responses import FileResponse
from schemas.batida.BatidasErrorResponses import NotFoundErrorResponse
from typing import Literal
from services.InformeService import InformeService
import os

def eliminar_archivo(path: str):
    if os.path.exists(path):
        print("Se va a eliminar ela rchivo")
        os.remove(path)
        print(f"archivo eliminado correctamente: {path}")

router = APIRouter(
    tags=["Informes"],  
    responses={
        404: {"description": "Recurso no encontrado", "model": NotFoundErrorResponse},
    }
)

@router.get(
    "/informe/batida",
    summary="Generar informe de asistentes a batida",
    responses={
        200: {
            "content": {"application/pdf": {}}, 
            "description": "PDF o Excel generado correctamente"
        },
        400: {"description": "Batida no existe"},
        500: {"description": "Error interno del servidor"}
    }
)
async def generar_informe_batida(
    id_batida: int,
    tipo: Literal["pdf", "excel"],
    service: InformeService = Depends()
):
    try:
        ruta = await service.generar_informe_batida(id_batida, tipo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    return FileResponse(path=ruta, media_type=(
        "application/pdf" if tipo == "pdf" else 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ), filename=ruta.split(os.sep)[-1])




@router.get(
    "/informe/zona",
    summary="Generar informe de voluntarios en zona",
    responses={
        200: {
            "content": {"application/pdf": {}}, 
            "description": "PDF o Excel generado correctamente"
        },
        400: {"description": "Zona no existe"},
        500: {"description": "Error interno del servidor"}
    }
)
async def generar_informe_zona(
    id_zona: int,
    tipo: Literal["pdf", "excel"],
    service: InformeService = Depends()
):
    try:
        ruta = await service.generar_informe_zona(id_zona, tipo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    return FileResponse(path=ruta, media_type=(
        "application/pdf" if tipo == "pdf" else 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ), filename=ruta.split(os.sep)[-1])




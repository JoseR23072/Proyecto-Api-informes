from fastapi import APIRouter, Depends,BackgroundTasks,HTTPException
from fastapi.responses import FileResponse
from schemas.batida.BatidasErrorResponses import ValidationErrorResponse
from schemas.batida.BatidasErrorResponses import NotFoundErrorResponse,BusinessValidationErrorResponse,InternalServerErrorResponse
from typing import Literal
from services.InformeService import InformeService
import os
import logging
from schemas.informes.ErrorResponse import QueryValidationErrorBatidaResponse,QueryValidationErrorZonaResponse

def eliminar_archivo(path: str):
    if os.path.exists(path):
        logging.info("Se va a eliminar ela rchivo")
        os.remove(path)
        logging.info(f"archivo eliminado correctamente: {path}")



router = APIRouter(
    tags=["Informes"],  
    responses={
        404: {"description": "Recurso no encontrado", "model": NotFoundErrorResponse},
        500: {"description": "Error interno del servidor","model": InternalServerErrorResponse}
    }
)

@router.get(
    "/informe/batida",
    summary="Generar informe de asistentes a batida",
    description="Genera un PDF o Excel con los asistentes y lo devuelve para descarga.",
    responses={
        200: {
            "description": "Fichero generado correctamente",
            
            "headers": {
                "X-Message": {
                    "description": "Informe generado correctamente",
                    "schema": {"type": "data", "example": "example.pdf"}
                }
            }
        },
        400: {"description": "Batida no existe","model":BusinessValidationErrorResponse},
        422: {"description": "Error de validación de datos de entrada", "model": QueryValidationErrorBatidaResponse},
    }
)
async def generar_informe_batida(
    background_tasks: BackgroundTasks,
    id_batida: int,
    formato: Literal["pdf", "excel"],
    service: InformeService = Depends(),
    
):
    try:
        ruta = await service.generar_informe_batida(id_batida, formato)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    background_tasks.add_task(eliminar_archivo, ruta)
    tipo_archivo = (
        "application/pdf"
        if formato == "pdf"
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    filename = os.path.basename(ruta)

    return FileResponse(
        path=ruta, 
        media_type=tipo_archivo, 
        filename=filename,
        background=background_tasks,
        headers={"X-Message": "Informe batida generado correctamente"}
    )




@router.get(
    "/informe/zona",
    summary="Generar informe de voluntarios en zona",
    description="Genera un PDF o Excel con los voluntarios registrados en la zona indicada, y lo devuelve para descarga.",

    responses={
        200: {
            "description": "Fichero generado correctamente",
            "headers": {
                "X-Message": {
                    "description": "Mensaje de éxito",
                    "schema": {"type": "string", "example": "Informe generado correctamente"}
                }
            }
        },
        400: {
            "description": "Zona no existe o tipo inválido",
            "model": ValidationErrorResponse
        },
        422: {
            "description": "Error de validación de parámetros de consulta (query)",
            "model": QueryValidationErrorZonaResponse
        }
    }
)
async def generar_informe_zona(
    background_tasks: BackgroundTasks,
    id_zona: int,
    formato: Literal["pdf", "excel"],
    service: InformeService = Depends()
):
    try:
        ruta = await service.generar_informe_zona(id_zona, formato)
    except ValueError as e:
        # Validaciones de negocio: zona inexistente o formato incorrecto
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        # Errores internos
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    background_tasks.add_task(eliminar_archivo, ruta)

    tipo_archivo = (
        "application/pdf"
        if formato == "pdf"
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    filename = os.path.basename(ruta)

    return FileResponse(path=ruta, 
        media_type=tipo_archivo, 
        filename=filename,
        headers={"X-Message": "Informe zona generado correctamente"},
        background=background_tasks
    )




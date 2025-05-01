from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
import datetime
from typing import Optional

from services.UtilitiesService import UtilitiesService
from config.schedulerConfiguration import modificar_horario, scheduler,TAREA_ID
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService

router = APIRouter(
    prefix="/utilidades",
    tags=["Utilidades"]
)

# DTOs
class SchedulerTimeDto(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hora en formato 0-23")
    minute: int = Field(..., ge=0, le=59, description="Minuto en formato 0-59")

class SchedulerTimeResponseDto(BaseModel):
    hour: int = Field(..., description="Hora programada")
    minute: int = Field(..., description="Minuto programado")
    next_run: Optional[datetime.datetime] = Field(None, description="Próxima ejecución programada")

class ManualResponseDto(BaseModel):
    code: int = Field(20000, description="Código de éxito para envío manual")
    message: str = Field(..., description="Mensaje confirmando envío manual")

# Endpoint: modificar horario del scheduler
@router.patch(
    "/reprogramarTarea",
    response_model=SchedulerTimeResponseDto,
    summary="Modificar horario del envío de recordatorios",
    description="Actualiza la hora y minuto en que el scheduler envía recordatorios diarios.",
    responses={
        200: {"description": "Horario actualizado correctamente", "model": SchedulerTimeResponseDto},
        422: {"description": "Parámetros de tiempo inválidos", "model": ManualResponseDto}
    }
)
async def reprogramar_tarea(
    dto: SchedulerTimeDto
) -> SchedulerTimeResponseDto:
    try:
        # Reprogramar
        modificar_horario(dto.hour, dto.minute)
        # Obtener próxima ejecución
        job = scheduler.get_job(TAREA_ID)
        next_run = job.next_run_time if job else None
        return SchedulerTimeResponseDto(
            hour=dto.hour,
            minute=dto.minute,
            next_run=next_run
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al reprogramar scheduler")

# Endpoint: envío manual de recordatorio para una batida
@router.post(
    "/scheduler/manual/{id_batida}",
    response_model=ManualResponseDto,
    summary="Enviar recordatorio manual",
    description="Genera y envía manualmente un recordatorio para la batida especificada.",
    responses={
        200: {"description": "Recordatorio enviado con éxito", "model": ManualResponseDto},
        404: {"description": "Batida no encontrada", "model": ManualResponseDto},
        500: {"description": "Error interno al enviar recordatorio", "model": ManualResponseDto}
    }
)
async def send_manual_reminder(
    id_batida: int,
    utils: UtilitiesService = Depends(),
    batida_svc: BatidaService = Depends()
) -> ManualResponseDto:
    try:
        batida: BatidaResponseDto = await batida_svc.ver_batida(id_batida)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        await utils.enviar_recordatorio_manual(batida)
        return ManualResponseDto(code=20000, message=f"Recordatorio enviado para batida {id_batida}")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al enviar recordatorio manual")

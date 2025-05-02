from fastapi import APIRouter, HTTPException, Depends,status
from schemas.batida.BatidasErrorResponses import InternalServerErrorResponse,NotFoundErrorResponse
from services.UtilitiesService import UtilitiesService
from config.schedulerConfiguration import modificar_horario, scheduler,TAREA_ID
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from services.BatidaService import BatidaService
from schemas.utilities.Responses import SchedulerTimeResponseDto,SchedulerTimeDto,ValidationErrorReprogramarTareaResponse,EnvioRecordatorioResponseDto,BatidaNotFoundResponse,PathParamUtilitiesValidationErrorResponse
from schemas.Voluntario import VoluntarioDto

router = APIRouter(
    prefix="/utilidades",
    tags=["Utilidades"],
    responses={
        404: {"description": "Recurso no encontrado", "model": NotFoundErrorResponse},
        500: {"description": "Error interno del servidor","model": InternalServerErrorResponse}
    }
)



# Endpoint: modificar horario del scheduler
@router.patch(
    "/reprogramarTarea",
    response_model=SchedulerTimeResponseDto,
    summary="Modificar horario del envío de recordatorios",
    description="Actualiza la hora y minuto en que el scheduler envía recordatorios diarios.",
    responses={
        200: {"description": "Horario actualizado correctamente", "model": SchedulerTimeResponseDto},
        422: {"description": "Parámetros de tiempo inválidos", "model": ValidationErrorReprogramarTareaResponse}
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
        proxima_tarea = job.next_run_time if job else None
        return SchedulerTimeResponseDto(
            hora=dto.hora,
            minuto=dto.minuto,
            proxima_tarea=proxima_tarea
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al reprogramar scheduler")



# Endpoint: envío manual de recordatorio para una batida
@router.post(
    "/enviar_recordatorio_manual/{id_batida}",
    response_model=EnvioRecordatorioResponseDto,
    summary="Enviar recordatorio manual",
    description="Genera y envía manualmente un recordatorio para la batida especificada.",
    responses={
        200: {"description": "Recordatorio enviado con éxito", "model": EnvioRecordatorioResponseDto},
        400: {"description": "Batida no encontrada", "model": BatidaNotFoundResponse},
        422: {"description": "Error de validación de parámetros de ruta", "model": PathParamUtilitiesValidationErrorResponse}
    }
)
async def enviar_recordario_batida_manual(
    id_batida: int,
    utils: UtilitiesService = Depends(),
    batida_svc: BatidaService = Depends()
) -> EnvioRecordatorioResponseDto:
    try:
        batida: BatidaResponseDto = await batida_svc.ver_batida(id_batida)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        await utils.enviar_recordatorio_manual(batida)
        return EnvioRecordatorioResponseDto(code=20000, message=f"Recordatorio enviado para batida {id_batida}")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al enviar recordatorio manual")


@router.post(
    "/enviar_codigo",
    summary="Enviar código de voluntario por email",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Email enviado correctamente (sin contenido en body)"},
        422: {"description": "Error de validación de entrada (formato JSON o tipos)"},
        
    }
)
async def send_volunteer_code(
    voluntario_dto: VoluntarioDto,
    utils: UtilitiesService = Depends()
):
    """
    Recibe un VoluntarioDto (por ejemplo extraído del microservicio de voluntarios)
    y envía su email de bienvenida con su numerovoluntario.
    """
    try:
        await utils.enviar_email_codigo_voluntario(voluntario_dto)
        
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Error interno al enviar el email")
    
    
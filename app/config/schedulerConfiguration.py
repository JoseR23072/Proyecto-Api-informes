from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import date,timedelta
from services.MicroserviciosService import MicroserviciosService
from typing import List,Dict
from models.Batida import BatidaEntity
import pytz
import logging
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from schemas.Voluntario import VoluntarioDto
from models.Batida import BatidaEntity
from services.UtilitiesService import UtilitiesService
from utils.enviar_recordatorios_asistencia_batidas import enviar_recordatorios_diarios
from repository.BatidaRepository import BatidaRepository
from config.database import get_session


scheduler = AsyncIOScheduler()
TAREA_ID="enviar_recordatorios_diarios"




def iniciar_scheduler():
    """
    Configura y arranca las tareas programadas en el scheduler.
    """


    # Programar la tarea diaria
    scheduler.add_job(
        enviar_recordatorios_batidas,
        CronTrigger(hour=22, minute=28, timezone=pytz.timezone("Europe/Madrid")),
        name="Enviar recordatorios diarios",
        id=TAREA_ID,
        replace_existing=True,
    )

    scheduler.start()
    logging.info("Scheduler iniciado.")


def modificar_horario(hour: int, minute: int):
    """
    Reprograma el job existente con nuevo horario.

    :param hour: hora (0-23)
    :param minute: minuto (0-59)
    :raises ValueError: si fuera de rango
    """
    

    # Crear nuevo trigger y reprogramar
    new_trigger = CronTrigger(hour=hour, minute=minute, timezone=pytz.timezone("Europe/Madrid"))
    scheduler.reschedule_job(job_id=TAREA_ID, trigger=new_trigger)
    logging.info("Scheduler job '%s' reprogramado a %02d:%02d", TAREA_ID, hour, minute)


def detener_scheduler():
    """
    Detiene el scheduler de forma ordenada.
    """
    scheduler.shutdown(wait=False)
    logging.info("Scheduler detenido.")



async def enviar_recordatorios_batidas() -> None:
        
        next_day = date.today() + timedelta(days=1)
        batidas_del_proximo_dia: List[BatidaResponseDto] = await buscar_batidas_por_fecha(next_day)
        if batidas_del_proximo_dia:
            await enviar_recordatorios_diarios(batidas_del_proximo_dia)
        


async def buscar_batidas_por_fecha(fecha:date) -> List[BatidaResponseDto]:
    session_gen = get_session()
    session=next(session_gen)
    try:
        repository = BatidaRepository(session)

        # 2) Ahora esto ya funciona, porque session es un Session real
        entidades: List[BatidaEntity] = repository.buscar_batidas_por_fecha(fecha)
        if not entidades:
            return None
        
        id_batidas = [e.id for e in entidades]
        all_ids = repository.obtener_voluntarios_distintos(id_batidas)

        voluntarios_info = await MicroserviciosService.obtener_datos_voluntarios(all_ids)
        voluntario_map: Dict[int, VoluntarioDto] = {v.id: v for v in voluntarios_info}

        lista_completa: List[BatidaResponseDto] = []
        for ent in entidades:
            lista_ids = repository.obtener_voluntarios_por_batida(ent.id)
            lista_info_voluntarios = [
                voluntario_map[i] for i in lista_ids if i in voluntario_map
            ]
            zona = await MicroserviciosService.obtener_datos_zona(ent.id_zona)
            lista_completa.append(
                BatidaResponseDto(
                    id_batida=ent.id,
                    nombre=ent.nombre,
                    latitud=ent.latitud,
                    longitud=ent.longitud,
                    zona=zona,
                    voluntarios=lista_info_voluntarios,
                    estado=ent.estado,
                    fecha_evento=ent.fecha_evento,
                    descripcion=ent.descripcion,
                )
            )
        return lista_completa
    finally:
        session.close()
        try:
            next(session_gen)
        except StopIteration:
            pass
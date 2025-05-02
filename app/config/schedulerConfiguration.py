from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import pytz
import logging
from utils.enviar_recordatorios_asistencia_batidas import enviar_recordatorios_diarios
from fastapi import Depends
from services.UtilitiesService import UtilitiesService


# Crear el scheduler
scheduler = AsyncIOScheduler()
TAREA_ID="enviar_recordatorios_diarios"


def iniciar_scheduler():
    """
    Configura y arranca las tareas programadas en el scheduler.
    """

    async def tarea_programada(service: UtilitiesService=Depends()):
        await service.enviar_recordatorios_batidas()


    # Programar la tarea diaria
    scheduler.add_job(
        lambda: asyncio.create_task(tarea_programada()),
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

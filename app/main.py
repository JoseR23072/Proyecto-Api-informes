from fastapi import FastAPI
from rest import InformesRestController,BatidasRestController
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import pytz
from utils.eventos import enviar_recordatorios_diarios
from config.database import engine,create_db_and_tables

logging.basicConfig(level=logging.INFO)


# Crear un scheduler asíncrono (AsyncIOScheduler)
scheduler = AsyncIOScheduler()

# Agregar la tarea al scheduler para que se ejecute todos los días a las 6:00 AM.
scheduler.add_job(enviar_recordatorios_diarios, CronTrigger(hour=22, minute=28, timezone=pytz.timezone("Europe/Madrid")))



@asynccontextmanager
async def lifespan(app: FastAPI):
    #Se crean las tablas y se insertan datos de prueba
    create_db_and_tables()
    # Lógica de inicio: se inicia el scheduler.
    scheduler.start()
    logging.info("Scheduler iniciado.")
    
    # Permitir que la aplicación se ejecute mientras el scheduler está activo.
    yield #En caso de que el servicio se apage se procesaran estas instrucciones
    
    # Lógica de apagado: se detiene el scheduler de forma ordenada.
    scheduler.shutdown(wait=False)
    logging.info("Scheduler detenido.")


app = FastAPI(title="API Informes Batidas Voluntariado",lifespan=lifespan)

app.include_router(InformesRestController.router, prefix="/voluntarios", tags=["Voluntarios"])

app.include_router(BatidasRestController.router,prefix="/riverspain")


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Informes de Batidas"}

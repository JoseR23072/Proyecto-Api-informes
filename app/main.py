from fastapi import FastAPI
from rest import InformesRestController,BatidasRestController,UtilitiesRestController
from contextlib import asynccontextmanager

import logging

from config.database import create_db_and_tables
from config.eurekaConfig import iniciar_eureka
logging.basicConfig(level=logging.INFO)
from config.schedulerConfiguration import iniciar_scheduler,detener_scheduler




@asynccontextmanager
async def lifespan(app: FastAPI):
    #Se crean las tablas y se insertan datos de prueba
    create_db_and_tables()

    # Inicializa y realiza la conexión a eureka
    await iniciar_eureka()

    iniciar_scheduler() 
    
    #En caso que el servicio se detenga se ejecutara esto
    yield #En caso de que el servicio se apage se procesaran estas instrucciones
    
    detener_scheduler()


app = FastAPI(title="API Informes Batidas Voluntariado",lifespan=lifespan)

app.include_router(InformesRestController.router, prefix="/riverspain")

app.include_router(BatidasRestController.router,prefix="/riverspain")

app.include_router(UtilitiesRestController.router,prefix="/riverspain")

@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Informes de Batidas"}

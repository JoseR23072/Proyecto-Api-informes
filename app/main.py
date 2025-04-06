from fastapi import FastAPI
from app.rest import InformesRestController

app = FastAPI(title="API Informes Batidas Voluntariado")

app.include_router(InformesRestController.router, prefix="/voluntarios", tags=["Voluntarios"])

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Informes de Batidas"}

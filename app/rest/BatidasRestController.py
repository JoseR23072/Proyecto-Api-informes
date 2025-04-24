from fastapi import APIRouter,Depends
from schemas.Batida import BatidaDto
from services.BatidaService import BatidaService
from typing import Annotated


router=APIRouter()

ServiceBatida=Annotated[BatidaService,Depends(BatidaService)]


@router.post("/batida")
def crear_batida(batida:BatidaDto, service:ServiceBatida) -> BatidaDto:
    service.crear_batida(batida)
    return service.crear_batida(batida)


    
@router.get("/batida")
def get_batida():
    return None

@router.patch("/batida")
def modificar_batida():
    return None

@router.patch("/batida/apuntarse")
def apuntarse_batida():
    return None

@router.patch("/batida/desapuntarse")
def desapuntarse_batida():
    return None

@router.delete("/batida/{id}")
def eliminar_batida():
    return None

#aqui hay que comprobar si el usuario esta ya apuntado
@router.get("/batida/")
def comprobar_voluntario_batida():
    return None
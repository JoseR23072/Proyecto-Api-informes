from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.responses import JSONResponse
from schemas.Batida import BatidaDto,BatidaDTO2
from services.BatidaService import BatidaService
from typing import Annotated,List

from schemas.batida.BatidaResponseDto import BatidaResponseDto
from schemas.batida.BatidaCreateDto import BatidaCreateDto
from schemas.batida.BatidasErrorResponses import InternalServerErrorResponse,NotFoundErrorResponse,ValidationErrorResponse

router=APIRouter(prefix="/batidas",
    tags=["Batidas"],  
    responses={
        404: {"description": "Recurso no encontrado", "model": NotFoundErrorResponse},
    })

ServiceBatida=Annotated[BatidaService,Depends(BatidaService)]



@router.post("/batida",response_model=BatidaResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una nueva batida",
    description="Crea una batida con los datos proporcionados y retorna la batida creada con su ID generado.",
    responses={
        201: {"description": "Batida creada exitosamente", "model": BatidaResponseDto},
        400: {"description": "Datos inválidos o error de validación", "model": ValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    })
def crear_batida(batida: BatidaCreateDto, service: ServiceBatida) -> BatidaResponseDto:
    """
    Endpoint para crear una nueva batida.

    Args:
        batida (BatidaCreateDto): Datos de la batida a crear.
        service (ServiceBatida): Servicio inyectado para manejar la lógica de negocio.

    Returns:
        BatidaResponseDto: La batida creada con su ID y datos adicionales.

    Raises:
        HTTPException: Si los datos son inválidos (400) o ocurre un error interno (500).
    """
    try:
        return service.crear_batida(batida)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.get("/batida/{id_batida}", response_model=BatidaDto)
async def get_batida(id_batida: int, service: ServiceBatida) -> BatidaDto:
    return await service.ver_batida(id_batida)

@router.get("/batidas", response_model=List[BatidaDto])
async def get_batidas(service: ServiceBatida) -> List[BatidaDto]:
    return await service.ver_batidas()

@router.patch("/batida/")    
def modificar_batida(batida: BatidaDTO2, service: ServiceBatida):
    return service.modificar_batida(batida)


@router.patch("/batida/{id_batida}/{codigo_voluntario}/apuntarse")
async def apuntarse_batida(id_batida: int, codigo_voluntario: str, service: ServiceBatida):
    return await service.apuntarse(id_batida, codigo_voluntario)

@router.patch("/batida/{id_batida}/{codigo_voluntario}/desapuntarse")
async def desapuntarse_batida(id_batida: int, codigo_voluntario: str, service: ServiceBatida):
    return service.desapuntarse(id_batida, codigo_voluntario)

@router.get("/batida/{id_batida}/comprobar")
def comprobar_voluntario_batida(id_batida: int, codigo_voluntario: str, service: ServiceBatida):
    return service.comprobar_voluntario(id_batida, codigo_voluntario)

@router.delete("/batida/{id_batida}")
def eliminar_batida(id_batida: int, service: ServiceBatida):
    respuesta=service.eliminar_batida(id_batida)

    return respuesta

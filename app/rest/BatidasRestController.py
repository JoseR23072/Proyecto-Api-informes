from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.responses import JSONResponse
from schemas.Batida import BatidaDto,BatidaDTO2
from services.BatidaService import BatidaService
from typing import Annotated,List

from schemas.batida.BatidaResponseDto import BatidaResponseDto,BatidaGetResponseDto
from schemas.batida.BatidaCreateDto import BatidaCreateDto
from schemas.batida.BatidaUpdateDto import BatidaUpdateDto
from schemas.batida.BatidasErrorResponses import InternalServerErrorResponse,NotFoundErrorResponse,ValidationErrorResponse,UnprocessableEntityResponse,UnprocessableEntityResponseGet,NotBatidasFoundResponse

router=APIRouter(
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
        422: {"description": "Error de validación de datos de entrada", "model": UnprocessableEntityResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    })
async def crear_batida(batida: BatidaCreateDto, service: ServiceBatida) -> BatidaResponseDto:
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
    
@router.get(
    "/batida/{id_batida}",
    response_model=BatidaResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Obtener batida por ID",
    description="Recupera los detalles de una batida específica dado su ID.",
    responses={
        200: {"description": "Batida encontrada exitosamente", "model": BatidaGetResponseDto},
        404: {"description": "Batida no encontrada", "model": NotFoundErrorResponse},
        422: {"description": "Error de validación de entrada", "model": UnprocessableEntityResponseGet},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    }
)
async def get_batida(id_batida: int, service: ServiceBatida) -> BatidaResponseDto:
    """
    Endpoint para obtener una batida específica.

    Args:
        id_batida (int): ID de la batida a consultar.
        service (ServiceBatida): Servicio inyectado de batidas.

    Returns:
        BatidaDto: Información de la batida solicitada.

    Raises:
        HTTPException: Si la batida no se encuentra (404) o ocurre un error interno (500).
    """
    try:
        return await service.ver_batida(id_batida)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/batidas", response_model=List[BatidaGetResponseDto],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las batidas",
    description="Obtiene una lista de todas las batidas registradas.",
    responses={
        200: {"description": "Lista de batidas obtenida exitosamente", "model": List[BatidaGetResponseDto]},
        404: {"description": "No se encontraron batidas", "model": NotBatidasFoundResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    })
async def get_batidas(service: ServiceBatida) -> List[BatidaGetResponseDto]:
    """
    Endpoint para obtener todas las batidas.

    Args:
        service (ServiceBatida): Servicio de batidas inyectado.

    Returns:
        List[BatidaGetResponseDto]: Lista de batidas encontradas.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    try:
        batidas = await service.ver_batidas()
        if not batidas:
            raise HTTPException(status_code=404, detail="No se encontraron batidas.")
        return batidas
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")



@router.patch("/batida",
    response_model=BatidaResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Modificar una batida existente",
    description=(
        "Aplica cambios parciales a una batida existente. Solo se modifican los cambios en el cuerpo de la petición"
    ),
    responses={
        200: {"description": "Batida modificada exitosamente", "model": BatidaResponseDto},
        400: {"description": "Error de validación de negocio", "model": ValidationErrorResponse},
        404: {"description": "Batida no encontrada", "model": NotFoundErrorResponse},
        422: {"description": "Error de validación de entrada", "model": UnprocessableEntityResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    })    
async def modificar_batida(batida: BatidaUpdateDto, service: ServiceBatida) -> BatidaResponseDto:
    """
    Endpoint para modificar una batida existente.

    - **id_batida**: ID de la batida a modificar
    - El resto de campos son opcionales y se actualizan si se incluyen en el JSON.

    Raises:
        HTTPException 400: Errores de validación de negocio (zona o voluntarios no existen).
        HTTPException 404: Si la batida no existe.
        HTTPException 422: Error de validación de tipo o formato en la entrada.
        HTTPException 500: Error inesperado.
    """
    try:
        return await service.modificar_batida(batida)
    except ValueError as e:
        msg = str(e)
        if msg.startswith("La batida con ID"):
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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

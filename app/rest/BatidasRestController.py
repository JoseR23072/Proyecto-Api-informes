from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.responses import JSONResponse
from services.BatidaService import BatidaService
from typing import Annotated,List
from schemas.batida.BatidaResponseDto import BatidaResponseDto,BatidaGetResponseDto
from schemas.batida.BatidaCreateDto import BatidaCreateDto
from schemas.batida.BatidaUpdateDto import BatidaUpdateDto
from schemas.batida.ApuntarseResponseDto import ApuntarseResponseDto
from schemas.batida.BatidasErrorResponses import InternalServerErrorResponse,NotFoundErrorResponse,ValidationErrorResponse,UnprocessableEntityResponse,UnprocessableEntityResponseGet,NotBatidasFoundResponse,VoluntarioDuplicadoResponse,BatidaNotFoundResponse,PathParamValidationErrorResponse,VoluntarioValidationErrorResponse,VoluntarioNotFoundResponse,PathParamBatidaValidationErrorResponse,BatidaDeleteNotFoundResponse,BusinessValidationErrorResponse
from schemas.batida.BatidaZonaResponseDto import BatidaZonaResponseDto
from schemas.batida.BatidaDesapuntarseResponseDto import DesapuntarseResponseDto,VoluntarioNoApuntadoResponse
from schemas.batida.BatidaDeleteResponseDto import EliminarBatidaResponseDto
from schemas.batida.BatidasVoluntarioRequestDto import BatidasVoluntarioRequestDto

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
async def crear_batida(batida: BatidaCreateDto, service: BatidaService = Depends(BatidaService) ) -> BatidaResponseDto:
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
        return await service.crear_batida(batida)
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
        400: {
            "description": "Error de validación de negocio (batida no existe)",
            "model": BusinessValidationErrorResponse
        },
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
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/batidas", response_model=List[BatidaGetResponseDto],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las batidas",
    description="Obtiene una lista de todas las batidas registradas.",
    responses={
        200: {"description": "Lista de batidas obtenida exitosamente (puede estar vacía)", "model": List[BatidaGetResponseDto]},
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
        return await service.ver_batidas()
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
        200: {"description": "Batida modificada exitosamente", "model": BatidaUpdateDto},
        400: {"description": "Error de validación de negocio", "model": ValidationErrorResponse},
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
        HTTPException 422: Error de validación de tipo o formato en la entrada.
        HTTPException 500: Error inesperado.
    """
    try:
        return await service.modificar_batida(batida)
    except ValueError as e:
        msg = str(e)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch(
    "/batida/{id_batida}/{codigo_voluntario}/apuntarse",
    response_model=ApuntarseResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Apuntarse a una batida",
    description="Permite a un voluntario apuntarse a la batida indicada.",
    responses={
        200: {"description": "Voluntario apuntado exitosamente", "model": ApuntarseResponseDto},
        400: {"description": "Voluntario ya apuntado", "model": VoluntarioDuplicadoResponse},
        422: {"description": "Error de validación de parámetros de ruta", "model": PathParamValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    }
)

async def apuntarse_batida(
    id_batida: int,
    codigo_voluntario: str,
    service: ServiceBatida
) -> ApuntarseResponseDto:
    """
    Endpoint para apuntar un voluntario a una batida existente.

    Args:
        id_batida (int): ID de la batida.
        codigo_voluntario (str): Código del voluntario a apuntar.

    Returns:
        ApuntarseResponseDto: DTO con la lista actualizada y mensaje de confirmación.

    Raises:
        HTTPException 400: Voluntario ya apuntado.
        HTTPException 422: ID inválido.
        HTTPException 500: Error interno.
    """
    try:
        return await service.apuntarse(id_batida, codigo_voluntario)
    except ValueError as e:
        msg = str(e)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch(
    "/batida/{id_batida}/{codigo_voluntario}/desapuntarse",
    response_model=DesapuntarseResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Desapuntarse de una batida",
    description="Permite a un voluntario remover su inscripción de la batida especificada.",
    responses={
        200: {"description": "Voluntario desapuntado exitosamente", "model": DesapuntarseResponseDto},
        400: {"description": "El voluntario no estaba apuntado a la batida", "model": VoluntarioNoApuntadoResponse},
        422: {"description": "Error de validación de parámetros de ruta", "model": PathParamValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    }
)
async def desapuntarse_batida(
    id_batida: int,
    codigo_voluntario: str,
    service: ServiceBatida
) -> DesapuntarseResponseDto:
    try:
        return await service.desapuntarse(id_batida, codigo_voluntario)
    except ValueError as e:
        msg = str(e)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")



@router.post(
    "/batidas/verBatidasVoluntario",
    response_model=List[BatidaGetResponseDto],
    status_code=status.HTTP_200_OK,
    summary="Listar batidas de un voluntario",
    description="Devuelve las batidas a las que está apuntado el voluntario indicado.",
    responses={
        200: {
            "description": "Lista de batidas obtenida (vacía si no hay datos)",
            "model": List[BatidaGetResponseDto]
        },
        400: {
            "description": "Voluntario no existe",
            "model": VoluntarioNotFoundResponse
        },
        422: {"description": "Error de validación en el cuerpo de la petición", "model": VoluntarioValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    }
)
async def ver_batidas_voluntario(
    request: BatidasVoluntarioRequestDto,
    service: ServiceBatida
) -> List[BatidaResponseDto]:
    try:
        return await service.ver_batidas_por_voluntario(request)
    except ValueError as e:
        # Aquí solo valido existencia de voluntario
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")




@router.delete(
    "/batida/{id_batida}",
    response_model=EliminarBatidaResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Eliminar una batida",
    description="Elimina la batida con el ID especificado del sistema.",
    responses={
        200: {"description": "Batida eliminada exitosamente", "model": EliminarBatidaResponseDto},
        400: {"description": "Batida inexistente", "model": BatidaDeleteNotFoundResponse},
        422: {"description": "Error de validación de parámetros de ruta", "model": PathParamBatidaValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": InternalServerErrorResponse}
    }
)
def eliminar_batida(
    id_batida: int,
    service: ServiceBatida
) -> EliminarBatidaResponseDto:
    try:
        return service.eliminar_batida(id_batida)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.get(
    "/batidas/verBatidasZona",
    response_model=List[BatidaZonaResponseDto],
    status_code=status.HTTP_200_OK,
    summary="Listar batidas de una zona",
    description="Devuelve las batidas asociadas a la zona indicada por su ID.",
    responses={
        200: {
            "description": "Lista de batidas obtenida (vacía si no hay datos)",
            "model":List[BatidaZonaResponseDto]
        },
        400: {
            "description": "ID de una zona inexistente",
            "model":ValidationErrorResponse
        }
        
    }
)
async def listar_batidas_de_zona(
    id_zona:int,
    service: ServiceBatida
) -> List[BatidaResponseDto]:
    
    try:
        return await service.buscar_batidas_de_una_zona(id_zona)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
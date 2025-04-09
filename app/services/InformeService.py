from schemas.Voluntario import VoluntarioDto
from repository.InformeRepository import guardar_voluntario

def create_voluntario(voluntario: VoluntarioDto):
    entidad_voluntario= guardar_voluntario(voluntario)
    
    # Convertimos la entidad de SQLAlchemy/SQLModel a un diccionario
    voluntario_dict = entidad_voluntario.model_dump()  # Usar dict() si usas SQLModel

    # Validamos el objeto convertido usando Pydantic (VoluntarioDto)
    return VoluntarioDto(**voluntario_dict)

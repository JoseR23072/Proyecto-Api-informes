import pandas as pd
import os
from typing import List
from app.schemas.Voluntario import VoluntarioDto  # Asegúrate de importar tu DTO

def generar_excel_voluntarios(voluntarios: List[VoluntarioDto], output_dir: str) -> str:
    """
    Función que genera un archivo Excel con la información de los voluntarios usando Pandas.
    
    :param voluntarios: Lista de objetos VoluntarioDto.
    :param output_dir: Directorio donde se guardará el archivo Excel.
    :return: Ruta del archivo generado.
    """
    
    # Convertir la lista de objetos VoluntarioDto a un diccionario
    voluntarios_dict = [voluntario.model_dump() for voluntario in voluntarios]
    
    # Crear un DataFrame de Pandas a partir del diccionario
    df = pd.DataFrame(voluntarios_dict)
    
    # Definir la ruta del archivo Excel
    archivo_excel = f"{output_dir}/Voluntarios.xlsx"
    
    # Exportar el DataFrame a Excel
    df.to_excel(archivo_excel, index=False, engine='openpyxl')
    
    print(f"Archivo Excel generado en: {archivo_excel}")
    
    return archivo_excel


if __name__ == "__main__":
    # Crear algunos datos de prueba
    voluntarios_prueba = [
        VoluntarioDto(nombre="Ana", apellidos="Martínez", email="ana.martinez@example.com", dni="12345678A", numeroVoluntario="V001"),
        VoluntarioDto(nombre="Juan", apellidos="González", email="juan.gonzalez@example.com", dni="23456789B", numeroVoluntario="V002"),
        VoluntarioDto(nombre="Pedro", apellidos="Sánchez", email="pedro.sanchez@example.com", dni="34567890C", numeroVoluntario="V003"),
    ]
    
    current_dir=os.path.dirname(os.path.realpath(__file__))


    # Directorio donde se guardará el archivo
    output_dir = os.path.join(current_dir,"./salidas_excel")
    os.makedirs(output_dir,exist_ok=True)
    
    # Llamar a la función para generar el archivo Excel
    generar_excel_voluntarios(voluntarios_prueba, output_dir)
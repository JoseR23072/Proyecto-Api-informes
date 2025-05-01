import os
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from schemas.batida.BatidaResponseDto import BatidaResponseDto
from schemas.Ciudad import CiudadDto
from schemas.Voluntario import VoluntarioDto
from schemas.Zona import ZonaDto
import logging

logging.getLogger("fontTools.subset").setLevel(logging.WARNING)
logging.getLogger("fontTools.ttLib").setLevel(logging.WARNING)

def generar_pdf(batida: BatidaResponseDto) ->str:
    """
    Función para generar un pdf con la información de una única Batida.
    Devolvemos la ruta del archivo generado.

    """

    # Obtener la ruta absoluta del directorio del script actual (app/utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta al directorio de plantillas
    plantillas_dir = os.path.join(current_dir, "pdf_asistencia_batida")
    
    directorio_donde_guardar_pdf=os.path.join(current_dir,"salidas_pdf")

    # Crear directorio de salida si no existe
    os.makedirs(directorio_donde_guardar_pdf, exist_ok=True)

    # Crear un entorno Jinja2 con el directorio de plantillas
    env = Environment(loader=FileSystemLoader(plantillas_dir))
    
    # Cargar la plantilla
    template = env.get_template("template.html")
    
    # Obtener ruta absoluta al logo
    logo_path = os.path.join(plantillas_dir, "web-app-manifest-512x512.png")

    ruta_logo = f"file://{logo_path.replace(os.sep, '/')}"

    # Renderizar HTML
    html_content = template.render(
        batida=batida,
        ruta_logo=ruta_logo
    )

    
    
    # Nombre de archivo seguro
    safe_name = batida.nombre.replace(" ", "_").lower()
    if hasattr(batida.fecha_evento, "isoformat"):
        fecha_str = batida.fecha_evento.isoformat()
    else:
        fecha_str = str(batida.fecha_evento)
    file_name = f"{safe_name}_{fecha_str}_informe.pdf"
    output_path = os.path.join(directorio_donde_guardar_pdf, file_name)

    # Generar PDF
    HTML(string=html_content).write_pdf(output_path)

    return output_path




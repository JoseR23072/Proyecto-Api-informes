import os
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader
from schemas.Zona import ZonaDto
import logging

logging.getLogger("fontTools.subset").setLevel(logging.WARNING)
logging.getLogger("fontTools.ttLib").setLevel(logging.WARNING)

def generar_pdf_informe_zona(zona: ZonaDto) -> str:
    """
    Genera un PDF con la información de una Zona.
    Devuelve la ruta del archivo generado.
    """
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Rutas
    plantillas_dir = os.path.join(current_dir, "pdf_asistencia_batida")

    directorio_donde_guardar_pdf = os.path.join(current_dir, "salidas_pdf")
    os.makedirs(directorio_donde_guardar_pdf, exist_ok=True)

    # Entorno Jinja2
    env = Environment(loader=FileSystemLoader(plantillas_dir))
    template = env.get_template("template-zona.html")
    
    # Ruta al logo
    logo_path = os.path.join(plantillas_dir, "web-app-manifest-512x512.png")
    ruta_logo = f"file://{logo_path.replace(os.sep, '/')}"

    # Renderizar HTML
    html_content = template.render(
        zona=zona,
        ruta_logo=ruta_logo
    )

    # Nombre del archivo
    safe_name = zona.nombre.replace(" ", "_").lower()
    file_name = f"zona_{safe_name}_informe.pdf"
    output_path = os.path.join(directorio_donde_guardar_pdf, file_name)

    # Estilos adicionales
    css = CSS(string='@page { size: A4; margin: 0.5cm; }')

    # Generar PDF
    HTML(string=html_content).write_pdf(
        output_path,
        stylesheets=[css],
        presentational_hints=True
    )

    return output_path

# Código de prueba
if __name__ == "__main__":
    from schemas.Ciudad import CiudadDto
    from schemas.Voluntario import VoluntarioDto

    ciudad = CiudadDto(id=1, nombre="Madrid", latitud=40.4168, longitud=-3.7038)
    voluntarios = [
        VoluntarioDto(
            id=1,
            nombre="Juan",
            apellidos="Pérez",
            email="juan.perez@example.com",
            dni="12345678A",
            numerovoluntario="JV123456",
            rol="voluntario",
            fechacreacion=None
        ),
        VoluntarioDto(
            id=2,
            nombre="Ana",
            apellidos="Gómez",
            email="ana.gomez@example.com",
            dni="87654321B",
            numerovoluntario="AG876543",
            rol="voluntario",
            fechacreacion=None
        )
    ]
    zona = ZonaDto(
        id=1,
        nombre="Zona Norte",
        latitud=40.4168,
        longitud=-3.7038,
        voluntariosZona=voluntarios,
        ciudad=ciudad
    )

    ruta_pdf = generar_pdf_informe_zona(zona)
    print(f"PDF generado con éxito en: {ruta_pdf}")
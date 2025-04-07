import os
import requests
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Tu clave de API de Google


GOOGLE_MAPS_API_KEY = os.getenv("API_GOOGLE","API_KEY")

# Obtener la ruta absoluta del directorio del script actual (app/utils)
current_dir = os.path.dirname(os.path.abspath(__file__))

template_dir = os.path.join(current_dir, "pdf_recordatorio")

OUTPUT_DIR=os.path.join(current_dir,"salidas_pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def obtener_url_mapa(lat, lng):
    return (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={lat},{lng}&zoom=15&size=600x400&markers=color:blue%7C{lat},{lng}"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )
def obtener_enlace_como_llegar(lat, lng):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"

def generar_pdf_recordatorio(nombre_voluntario, nombre_batida, fecha, latitud,longitud,ciudad):
    # Obtener coordenadas y dirección formateada
    url_mapa = obtener_url_mapa(latitud, longitud)
    enlace_como_llegar = obtener_enlace_como_llegar(latitud, longitud)

    # Cargar y renderizar plantilla
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("template.html")

    html_renderizado = template.render(
        nombre_voluntario=nombre_voluntario,
        nombre_batida=nombre_batida,
        fecha=fecha,
        ciudad=ciudad,
        direccion=enlace_como_llegar,
        imagen_mapa=url_mapa
    )

    # Crear PDF
    nombre_archivo = f"{OUTPUT_DIR}/Recordatorio_{nombre_voluntario.replace(' ', '_')}.pdf"
    HTML(string=html_renderizado).write_pdf(nombre_archivo)

    print(f"PDF generado en: {nombre_archivo}")
    return nombre_archivo


if __name__ == "__main__":
    # Datos de prueba
    nombre_voluntario = "Ana Martínez"
    nombre_batida = "Batida Playa del Faro"
    fecha = "2025-04-10"
    ciudad = "Málaga"
    latitud = 36.7213
    longitud = -4.4214

    generar_pdf_recordatorio(nombre_voluntario, nombre_batida, fecha, latitud, longitud, ciudad)
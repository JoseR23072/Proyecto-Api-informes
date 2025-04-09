import os
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

def generar_pdf(nombre, zona, fecha, asistentes):
    # Obtener la ruta absoluta del directorio del script actual (app/utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta al directorio de plantillas
    plantillas_dir = os.path.join(current_dir, "pdf_asistencia_batida")
    
    # Crear un entorno Jinja2 con el directorio de plantillas
    env = Environment(loader=FileSystemLoader(plantillas_dir))
    
    # Cargar la plantilla
    template = env.get_template("template.html")
    
    # Generar el HTML para los asistentes
    asistentes_html = ""
    for asistente in asistentes:
        asistentes_html += "<tr><td>{id}</td><td>{numero_voluntario}</td><td>{nombre}</td></tr>".format(
            id=asistente['id'],
            numero_voluntario=asistente['numero_voluntario'],
            nombre=asistente['nombre']
        )

    # Renderizar el HTML con Jinja2
    html_content = template.render(
        titulo=f"{nombre} - Informe de Batida",
        nombre=nombre,
        zona=zona,
        fecha=fecha,
        ruta_logo="file://" + os.path.join(plantillas_dir, "web-app-manifest-512x512.png").replace("\\", "/"),
        asistentes_html=asistentes_html
    )
    
    # Crear el PDF usando WeasyPrint
    file_name = f"{nombre.replace(' ', '_')}_informe.pdf"
    HTML(string=html_content).write_pdf(file_name)

    return file_name


if __name__ == "__main__":
    nombre = "Batida del Río"
    zona = "Zona A"
    fecha = "2025-04-06"
    asistentes = [
        {"id": 1, "numero_voluntario": "12345", "nombre": "Juan Pérez"},
        {"id": 2, "numero_voluntario": "67890", "nombre": "Ana Gómez"},
        {"id": 3, "numero_voluntario": "54321", "nombre": "Carlos Martínez"}
    ]

    archivo_pdf = generar_pdf(nombre, zona, fecha, asistentes)
    print(f"PDF generado con éxito: {archivo_pdf}")

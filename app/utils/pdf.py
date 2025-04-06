from xhtml2pdf import pisa

def generar_pdf(nombre, zona, fecha, asistentes):
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{nombre} - Informe de Batida</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}

            .header {{
                background-color: #f2f2f2;
                padding: 10px;
            }}

            .contenedor-logo img {{
                height: 100px;
                border-radius: 50px;
            }}

            .header {{
                display: flex;
                gap: 30px;
            }}

            .subcontenedor-h1 {{
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
            }}

            .contenedor-h1 {{
                width: 100%;
            }}

            .container-info {{
                display: flex;
                justify-content: space-between;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}

            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="contenedor-logo">
                <img src="./web-app-manifest-512x512.png" alt="">
            </div>
            <div class="contenedor-h1">
                <div class="subcontenedor-h1">
                    <h1>RiverSpain</h1>
                </div>
            </div>
        </div>
        <div class="container-info">
            <div>
                <p>Nombre batida: {nombre}</p>
            </div>
            <div>
                <p>Zona: {zona}</p>
            </div>
            <div>
                <p>Fecha: {fecha}</p>
            </div>
        </div>
        <p>Lista de asistentes:</p>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Número de voluntario</th>
                    <th>Nombre</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Iterar sobre los asistentes y agregar filas al HTML
    for asistente in asistentes:
        html_content += f"""
            <tr>
                <td>{asistente['id']}</td>
                <td>{asistente['numero_voluntario']}</td>
                <td>{asistente['nombre']}</td>
            </tr>
        """
    
    # Cerrar el contenido de la tabla y el HTML
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Convertir el HTML a PDF
    file_name = f"{nombre}_informe.pdf"
    with open(file_name, "wb") as output_file:
        pisa.CreatePDF(html_content, dest=output_file)

    return file_name

if __name__ == "__main__":
    # Datos de prueba para la generación del informe
    nombre = "Batida del Río"
    zona = "Zona A"
    fecha = "2025-04-06"
    asistentes = [
        {"id": 1, "numero_voluntario": "12345", "nombre": "Juan Pérez"},
        {"id": 2, "numero_voluntario": "67890", "nombre": "Ana Gómez"},
        {"id": 3, "numero_voluntario": "54321", "nombre": "Carlos Martínez"}
    ]

    # Llamar a la función para generar el PDF
    archivo_pdf = generar_pdf(nombre, zona, fecha, asistentes)

    # Imprimir el nombre del archivo generado
    print(f"PDF generado con éxito: {archivo_pdf}")
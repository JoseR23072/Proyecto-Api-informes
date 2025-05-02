from pathlib import Path
import pandas as pd
from typing import Union
from schemas.Zona import ZonaDto
from schemas.Voluntario import VoluntarioDto
from datetime import datetime
import os

# Obtener la ruta absoluta del directorio del script actual (app/utils)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta al directorio de plantillas

output_path=os.path.join(current_dir,"salidas_excel")
os.makedirs(output_path, exist_ok=True)

def generar_excel_informe_zona(
    zona: ZonaDto,
) -> str:
    """
    Genera un archivo Excel con dos hojas:
      - Resumen de la zona (metadata)
      - Lista de voluntarios (detallada)

    Args:
        zona (ZonaDto): DTO con información completa de la zona.
        output_dir (str | Path): Directorio donde guardar el archivo.

    Returns:
        str: Ruta completa al archivo Excel generado.
    """

    

    # 1) Hoja de Resumen
    resumen_data = {
        "Campo": [
            "ID Zona",
            "Nombre",
            "Latitud",
            "Longitud",
            "Ciudad",
            "Número de Voluntarios"
        ],
        "Valor": [
            zona.id,
            zona.nombre,
            zona.latitud,
            zona.longitud,
            zona.ciudad.nombre,
            len(zona.voluntariosZona)
        ]
    }
    df_resumen = pd.DataFrame(resumen_data)

    # 2) Hoja de Voluntarios
    # Convertir DTOs a dicts y DataFrame
    voluntarios_dict = []
    for v in zona.voluntariosZona:
        voluntarios_dict.append({
            "ID": v.id,
            "Número Voluntario": v.numerovoluntario,
            "Nombre": v.nombre,
            "Apellidos": v.apellidos,
            "DNI": v.dni,
            "Email": v.email,
            "Rol": v.rol or "",
            "Fecha Creación": v.fechacreacion.isoformat() if v.fechacreacion else ""
        })
    df_vol = pd.DataFrame(voluntarios_dict)

    # Nombre de archivo
    safe_name = "_".join(zona.nombre.lower().split())
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"zona_{safe_name}_{date_str}_informe.xlsx"
    file_path = os.path.join(output_path,file_name)

    # Escribir Excel con dos hojas y formato básico
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        # Resumen
        df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
        # Voluntarios
        df_vol.to_excel(writer, sheet_name="Voluntarios", index=False)

        # Ajustes en ambas hojas
        for sheet_name in ["Resumen", "Voluntarios"]:
            sheet = writer.sheets[sheet_name]
            # Freeze header row
            sheet.freeze_panes = sheet["A2"]
            # Ajustar ancho de columnas
            for col_cells in sheet.columns:
                max_length = max(
                    len(str(cell.value)) if cell.value is not None else 0
                    for cell in col_cells
                ) + 2
                sheet.column_dimensions[col_cells[0].column_letter].width = max_length

    return str(file_path)


if __name__ == "__main__":
    from schemas.Ciudad import CiudadDto
    from schemas.Voluntario import VoluntarioDto
    from schemas.Zona import ZonaDto
    from datetime import date

    # Crear datos de prueba
    ciudad = CiudadDto(id=1, nombre="Madrid", latitud=40.4168, longitud=-3.7038)
    voluntarios = [
        VoluntarioDto(id=1, nombre="Juan", apellidos="Pérez", email="juan.perez@example.com",
                      dni="12345678A", numerovoluntario="JV001", rol="voluntario", fechacreacion=None),
        VoluntarioDto(id=2, nombre="Ana", apellidos="Gómez", email="ana.gomez@example.com",
                      dni="87654321B", numerovoluntario="AG002", rol="organizador", fechacreacion=date.today())
    ]
    zona = ZonaDto(
        id=1,
        nombre="Zona Norte",
        latitud=40.4168,
        longitud=-3.7038,
        voluntariosZona=voluntarios,
        ciudad=ciudad
    )

    # Generar el informe
    ruta = generar_excel_informe_zona(zona)
    print(f"Excel generado en: {ruta}")
import fitz
from datetime import datetime

def extraer_oficio_y_asunto_primera_pagina(ruta_pdf):
    try:
        documento_pdf = fitz.open(ruta_pdf)
        primera_pagina = documento_pdf[0]
        texto_primera_pagina = primera_pagina.get_text()
        parrafos = [parrafo.strip() for parrafo in texto_primera_pagina.split('\n') if parrafo.strip()]

        indice_oficio = next((i for i, linea in enumerate(parrafos) if "Oficio No." in linea), None)
        indice_fecha = next((i for i, linea in enumerate(parrafos) if "Monterrey, N.L., a" in linea), None)
        indice_asunto = next((i for i, linea in enumerate(parrafos) if "Asunto:" in linea), None)

        oficio = parrafos[indice_oficio].replace("Oficio No.", "") if indice_oficio is not None else None
        fecha = parrafos[indice_fecha].replace("Monterrey, N.L., a", "") if indice_fecha is not None else None

        fecha_objeto = fecha.split(' ');
        fecha_lista_filtrada = [elemento for elemento in fecha_objeto if elemento and elemento.lower() != "de"]

        asunto_lines = parrafos[indice_asunto + 0:] if indice_asunto is not None else []
        asunto = " ".join(asunto_lines[:4]) if len(asunto_lines) > 4 else None


        documento_pdf.close()

        return {
            "NUMCODE": 0,
            "STRMESSAGE": "Exito",
            "RESPONSE": [
                {"Oficio": oficio,
                 "Fecha": {"dia": fecha_lista_filtrada[0], "mes": fecha_lista_filtrada[1], "anio": fecha_lista_filtrada[2]},
                 "Asunto": asunto.replace("Asunto:", "")}
            ],
            "SUCCESS": True
        }

    except Exception as e:
        return {
            "NUMCODE": 0,
            "STRMESSAGE": f"Error al leer el archivo PDF: {e}",
            "RESPONSE": [],
            "SUCCESS": False
        }

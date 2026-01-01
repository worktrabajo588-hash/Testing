import pdfplumber
import re

def analizar_resultados(datos):
    analisis = []

    RANGOS = {
        'hemoglobina': {
            'min': 12.0, 'max': 16.0, 'label': 'Hemoglobina'
        },
        'leucocitos_totales': {
            'min': 4.5, 'max': 11.0, 'label': 'Leucocitos'
        },
        'plaquetas': {
            'min': 150.0, 'max': 450.0, 'label': 'Plaquetas'
        },
        'globulos_rojos': {
            'min': 4.2, 'max': 5.4, 'label': 'Glóbulos Rojos'
        },
    }

    for clave, info in RANGOS.items():
        valor = datos.get(clave)

        # Estado por defecto
        estado = "Normal"
        clase = "estado-normal"
        mensaje = "Dentro del rango normal."

        if valor is None:
            estado = "No detectado"
            clase = "alerta-baja"
            mensaje = "No se pudo leer este valor del documento."

        elif valor < info['min']:
            estado = "Bajo"
            clase = "alerta-baja"
            mensaje = f"Bajo el rango normal ({info['min']})."

        elif valor > info['max']:
            estado = "Alto"
            clase = "alerta-alta"
            mensaje = f"Sobre el rango normal ({info['max']})."

        analisis.append({
            'nombre': info['label'],
            'valor': valor if valor is not None else "—",
            'estado': estado,
            'mensaje': mensaje,
            'clase': clase
        })

    return analisis

def extraer_texto_pdf(archivo_pdf):
    """
    Extrae todo el texto del PDF y lo deja en una sola línea limpia
    """
    texto = ""
    with pdfplumber.open(archivo_pdf) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                texto += " " + page_text

    # Limpieza básica
    texto = texto.replace('\n', ' ')
    texto = re.sub(r'\s+', ' ', texto)  # espacios dobles
    texto = texto.replace('■', '³')     # corrección típica de encoding

    return texto.strip()

def buscar_valor(texto, etiqueta):
    """
    Busca un valor numérico después de una etiqueta (ej: Hemoglobina 11.1)
    """
    patron = rf"{etiqueta}\s+([\d]+(?:\.[\d]+)?)"
    match = re.search(patron, texto, re.IGNORECASE)
    return float(match.group(1)) if match else None

def extraer_hemograma(texto):
    return {
        # SERIE ROJA
        "globulos_rojos": buscar_valor(texto, "Glóbulos Rojos"),
        "hemoglobina": buscar_valor(texto, "Hemoglobina"),
        "hematocrito": buscar_valor(texto, "Hematocrito"),
        "vmc": buscar_valor(texto, "VMC"),
        "hcm": buscar_valor(texto, "HCM"),
        "chcm": buscar_valor(texto, "CHCM"),

        # PLAQUETAS
        "plaquetas": buscar_valor(texto, "Plaquetas"),

        # SERIE BLANCA
        "leucocitos_totales": buscar_valor(texto, "Glóbulos Blancos"),
        "neutrofilos_p": buscar_valor(texto, "Neutrófilos"),
        "linfocitos_p": buscar_valor(texto, "Linfocitos"),
        "monocitos_p": buscar_valor(texto, "Monocitos"),
        "eosinofilos_p": buscar_valor(texto, "Eosinófilos"),
        "basofilos_p": buscar_valor(texto, "Basófilos"),
    }

import pdfplumber
import re

def analizar_resultados(datos):
    analisis = []

    RANGOS = {
    # SERIE ROJA
    'hemoglobina': {'min': 12.0, 'max': 16.0, 'label': 'Hemoglobina'},
    'hematocrito': {'min': 36.0, 'max': 47.0, 'label': 'Hematocrito'},
    'globulos_rojos': {'min': 4.1, 'max': 5.4, 'label': 'Glóbulos Rojos'},
    'vmc': {'min': 80.0, 'max': 100.0, 'label': 'VCM'},
    'hcm': {'min': 27.0, 'max': 33.0, 'label': 'HCM'},
    'chcm': {'min': 32.0, 'max': 36.0, 'label': 'CHCM'},

    # PLAQUETAS
    'plaquetas': {'min': 150.0, 'max': 450.0, 'label': 'Plaquetas'},

    # SERIE BLANCA
    'leucocitos_totales': {'min': 4.0, 'max': 11.0, 'label': 'Leucocitos'},
    'neutrofilos_p': {'min': 40.0, 'max': 70.0, 'label': 'Neutrófilos %'},
    'linfocitos_p': {'min': 20.0, 'max': 45.0, 'label': 'Linfocitos %'},
    'monocitos_p': {'min': 2.0, 'max': 10.0, 'label': 'Monocitos %'},
    'eosinofilos_p': {'min': 1.0, 'max': 6.0, 'label': 'Eosinófilos %'},
    'basofilos_p': {'min': 0.0, 'max': 1.0, 'label': 'Basófilos %'},
}

    CAUSAS = {
        "hemoglobina": {
            "alta": [
                "Deshidratación",
                "Policitemia vera",
                "Tabaquismo",
                "Vida en altura",
                "Enfermedad pulmonar crónica",
                "Tumores productores de eritropoyetina"
            ],
            "baja": [
                "Anemia ferropénica",
                "Sangrado agudo o crónico",
                "Déficit de vitamina B12 o folato",
                "Insuficiencia renal",
                "Enfermedad crónica",
                "Embarazo"
            ]
        },
        "leucocitos_totales": {
            "alta": [
                "Infección bacteriana",
                "Inflamación",
                "Estrés físico o emocional",
                "Uso de corticoides",
                "Leucemia"
            ],
            "baja": [
                "Infección viral",
                "Inmunosupresión",
                "Quimioterapia",
                "Aplasia medular",
                "Déficit de vitamina B12"
            ]
        },
        "plaquetas": {
            "alta": [
                "Inflamación",
                "Infección",
                "Post cirugía",
                "Ferropenia",
                "Trombocitosis esencial"
            ],
            "baja": [
                "Púrpura trombocitopénica inmune",
                "Infección viral",
                "Enfermedad hepática",
                "Alcoholismo",
                "Déficit de B12 o folato"
            ]
        },
        "globulos_rojos": {
            "alta": [
                "Deshidratación",
                "Policitemia",
                "Hipoxia crónica",
                "Tabaquismo"
            ],
            "baja": [
                "Anemia",
                "Hemorragia",
                "Enfermedad renal",
                "Déficit nutricional"
            ] 
            },
            
    "hematocrito": {
        "alta": [
            "Deshidratación",
            "Policitemia",
            "Tabaquismo",
            "Hipoxia crónica"
        ],
        "baja": [
            "Anemia",
            "Sangrado",
            "Embarazo",
            "Hiperhidratación",
            "Falla medular"
        ]
    },

    "vmc": {
        "alta": [
            "Déficit de vitamina B12",
            "Déficit de folato",
            "Alcoholismo",
            "Hipotiroidismo",
            "Hepatopatía"
        ],
        "baja": [
            "Ferropenia",
            "Talasemias",
            "Anemia sideroblástica",
            "Intoxicación por plomo"
        ]
    },

    "hcm": {
        "alta": [
            "Macrocitosis",
            "Alcoholismo",
            "Hepatopatía"
        ],
        "baja": [
            "Ferropenia",
            "Talasemias",
            "Anemia crónica"
        ]
    },

    "chcm": {
        "alta": [
            "Esferocitosis",
            "Hemólisis severa",
            "Quemaduras"
        ],
        "baja": [
            "Hipocromía",
            "Ferropenia",
            "Talasemia",
            "Anemia sideroblástica"
        ]
    },

    "neutrofilos_p": {
        "alta": [
            "Infección bacteriana",
            "Estrés",
            "Inflamación",
            "Corticoides"
        ],
        "baja": [
            "Virosis",
            "Fármacos",
            "Déficit de B12 o folato",
            "Aplasia medular"
        ]
    },

    "linfocitos_p": {
        "alta": [
            "Infección viral",
            "Tos ferina",
            "Hipertiroidismo"
        ],
        "baja": [
            "Estrés",
            "Corticoides",
            "VIH",
            "Quimioterapia",
            "Desnutrición"
        ]
    },

    "monocitos_p": {
        "alta": [
            "Tuberculosis",
            "Infecciones crónicas",
            "Inflamación",
            "Recuperación post-quimioterapia"
        ],
        "baja": []
    },

    "eosinofilos_p": {
        "alta": [
            "Alergias",
            "Parásitos",
            "Fármacos",
            "Enfermedad celíaca"
        ],
        "baja": []
    },

    "basofilos_p": {
        "alta": [
            "Alergias",
            "Trastornos mieloproliferativos",
            "Hipotiroidismo"
        ],
        "baja": []
    }
}
        

    for clave, info in RANGOS.items():
        valor = datos.get(clave)
        causas = []

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
            causas = CAUSAS.get(clave, {}).get("baja", [])

        elif valor > info['max']:
            estado = "Alto"
            clase = "alerta-alta"
            mensaje = f"Sobre el rango normal ({info['max']})."
            causas = CAUSAS.get(clave, {}).get("alta", [])

        analisis.append({
            'nombre': info['label'],
            'valor': valor if valor is not None else "—",
            'estado': estado,
            'mensaje': mensaje,
            'clase': clase,
            'causas': causas
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
    
def extraer_datos_paciente(texto):

    def buscar(patron):
        match = re.search(patron, texto, re.IGNORECASE)
        return match.group(1).strip() if match else "No encontrado"

    return {
        "nombre_completo": buscar(
            r'Nombre\s+Completo\s+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s+Identificación'
        ),

        "identificacion": buscar(
            r'Identificación\s*\(.*?\)\s*([\w\-]+)'
        ),

        "genero_sexo": buscar(
            r'Género\s+(Masculino|Femenino)'
        ),

        "edad": buscar(
            r'Edad\s+(\d+)'
        ),

        "fecha_nacimiento": buscar(
            r'Fecha\s+de\s+Nacimiento\s+([\d/]+)'
        ),

        "procedencia": buscar(
            r'Procedencia\s+([A-Za-zÁÉÍÓÚáéíóúñÑ\s–\-]+?)\s+2\.\s+DATOS'
        )
    }

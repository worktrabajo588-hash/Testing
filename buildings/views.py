
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Hemograma
from pdfminer.high_level import extract_text # La forma más rápida y precisa
from .utils import analizar_resultados # La función de arriba
import io
import re
def index(request):
    return render(request, 'buildings/index.html')

def building_detail(request, building_id):
    return render(request, 'buildings/detail.html')

def escanear(request):
    return render(request, 'buildings/escanear.html/')

def page2(request):
    return render(request, 'buildings/page2.html/')

def lector(request):
    return render(request, 'buildings/lector.html/')

def limpiar_y_extraer(texto_pdf):
    # 1. Quitamos comillas, saltos de línea y signos de dólar del PDF
    texto_limpio = texto_pdf.replace('"', '').replace('\n', ' ').replace('$', '')
    
    # 2. Diccionario de búsqueda con los nombres exactos del archivo
    patrones = {
        'globulos_rojos': r'Glóbulos Rojos:\s*([\d.]+)', # Captura 3.68. 
        'hemoglobina': r'Hemoglobina:\s*([\d.]+)',    # Captura 11.1 
        'hematocrito': r'Hematocrito:\s*([\d.]+)',    # Captura 34.0 
        'plaquetas': r'Plaquetas:\s*([\d.]+)',        # Captura 208 
        'leucocitos': r'Glóbulos Blancos:\s*([\d.]+)'  # Captura 10.02 [cite: 9]
    }
    
    resultados = {}
    for clave, patron in patrones.items():
        match = re.search(patron, texto_limpio)
        if match:
            # Quitamos el punto final si existe (como en el 3.68.) para poder convertir a float
            valor_limpio = match.group(1).rstrip('.')
            resultados[clave] = float(valor_limpio)
        else:
            resultados[clave] = 0.0
            
    return resultados

def lector_pdf_view(request):
    print("🔥 ENTRÓ AL VIEW lector_pdf_view")
    lista_analisis = []
    
    if request.method == 'POST' and request.FILES.get('archivo_pdf'):
        pdf_file = request.FILES['archivo_pdf']
        print("📄 ARCHIVO RECIBIDO")
        
        try:
            # 1. Extraer texto
            pdf_content = pdf_file.read()
            texto_bruto = extract_text(io.BytesIO(pdf_content))
            
            # 2. LIMPIEZA AGRESIVA (Clave para tu archivo)
            # Quitamos comillas, quitamos saltos de línea y normalizamos espacios
            texto_limpio = texto_bruto.replace('"', '').replace('\n', ' ')
            # Eliminamos puntos finales que estén pegados a números antes de espacios
            texto_limpio = re.sub(r'(\d+)\.(\s)', r'\1\2', texto_limpio)
            
            print(f"DEBUG - Texto procesado: {texto_limpio}") # Mira esto en tu terminal
            # Extraer TODOS los números (decimales incluidos)
            numeros = re.findall(r'\d+(?:\.\d+)?', texto_limpio)

            print("🔢 NÚMEROS ENCONTRADOS:", numeros)
            
            # 3. Función de búsqueda ultra-flexible
            def buscar(nombre):
                patron = rf"{nombre}[\s:]*([\d]+(?:\.[\d]+)?)"
                match = re.search(patron, texto_limpio, re.IGNORECASE)
                if match:
                    return float(match.group(1))
                return 0.0

            # 4. Mapeo con los nombres exactos de tu PDF
        
            datos = {
                'globulos_rojos': float(numeros[0]),
                'hemoglobina': float(numeros[1]),
                'hematocrito': float(numeros[2]),
                'plaquetas': float(numeros[6]),
                'leucocitos_totales': float(numeros[7]),
            }
            
            print(f"DEBUG - Datos extraídos: {datos}")
            
        except (IndexError, ValueError):
            datos = {}
            print("✅ DATOS FINALES:", datos)
    
            # 5. Analizar
        
            lista_analisis = analizar_resultados(datos)

        except Exception as e:
            print(f"ERROR CRÍTICO: {e}")

    return render(request, 'buildings/lector.html', {'lista_analisis': lista_analisis})

    
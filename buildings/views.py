from django.shortcuts import render, redirect
from .utils import analizar_resultados, extraer_texto_pdf, extraer_hemograma # La función de arriba

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


def lector_pdf_view(request):
    lista_analisis = []
    datos = {}

    if request.method == "POST" and request.FILES.get("archivo_pdf"):
        pdf_file = request.FILES["archivo_pdf"]

        try:
            # 1️⃣ Leer texto del PDF con pdfplumber
            texto = extraer_texto_pdf(pdf_file)

            # 2️⃣ Extraer datos del hemograma
            datos = extraer_hemograma(texto)

            # 3️⃣ Analizar resultados
            lista_analisis = analizar_resultados(datos)

        except Exception as e:
            print("ERROR al procesar PDF:", e)

    return render(request, "buildings/lector.html", {
        "lista_analisis": lista_analisis,
        "datos": datos

    })
    


from django.shortcuts import render
from django.conf import settings
from pdfminer.high_level import extract_text # La forma más rápida y precisa
import io

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
    texto_extraido = ""
    
    if request.method == 'POST' and request.FILES.get('archivo_pdf'):
        pdf_file = request.FILES['archivo_pdf']
        
        try:
            # 1. Leer el archivo desde la memoria (para que sea rápido en la demo)
            pdf_content = pdf_file.read()
            
            # 2. Usar pdfminer.six para sacar el texto
            # Usamos BytesIO para que pdfminer lo trate como un archivo abierto
            texto_extraido = extract_text(io.BytesIO(pdf_content))
            
            # Limpiamos un poco el texto para que no se vea feo en el HTML
            texto_extraido = texto_extraido.strip()
            
        except Exception as e:
            texto_extraido = f"Error al leer el PDF: {e}"

    return render(request, 'lector.html', {'texto': texto_extraido})

def leer_pdf(ruta_archivo):
    try:
        texto = extract_text(ruta_archivo)
        print(texto)
    except Exception as e:
        print(f"Error al leer el PDF: {e}")

leer_pdf("tu_archivo.pdf")
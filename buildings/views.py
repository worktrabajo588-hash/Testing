from datetime import timezone
import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AnalisisUploadForm
from .models import ResultadoPaciente
from .utils import extraer_texto_de_pdf, ocr_de_archivo, analizar_hemograma
from django.conf import settings
def index(request):
    return render(request, 'buildings/index.html')

def building_detail(request, building_id):
    # Lógica para obtener datos del edificio desde la base de datos
    return render(request, 'buildings/detail.html')

def escanear(request):
    # 1. MANEJAR LA SOLICITUD POST (Subida del archivo)
    if request.method == 'POST':
        form = AnalisisUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            archivo_subido = request.FILES['archivo_analisis']
            nombre_paciente = form.cleaned_data['nombre_paciente']
            
            # --- Lógica de Extracción ---
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_analisis', archivo_subido.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, 'wb+') as destination:
                for chunk in archivo_subido.chunks():
                    destination.write(chunk)
            
            texto_extraido = extraer_texto_de_pdf(temp_path)
            
            if not texto_extraido or len(texto_extraido.strip()) < 50:
                texto_extraido = ocr_de_archivo(temp_path)
            # --- Fin Lógica de Extracción ---

            if texto_extraido:
                resultados = analizar_hemograma(texto_extraido)
                
                ResultadoPaciente.objects.create(
                    nombre_paciente=nombre_paciente,
                    fecha_analisis=timezone.now().date(),
                    hb_resultado=resultados.get('hb_resultado'),
                    wbc_resultado=resultados.get('wbc_resultado'),
                    plt_resultado=resultados.get('plt_resultado')
                )
                os.remove(temp_path)
                return redirect('nombre_de_tu_ruta_de_exito') # Redirigir después de guardar
            else:
                form.add_error('archivo_analisis', 'No se pudo extraer texto del archivo.')
    
    # 2. MANEJAR LA SOLICITUD GET (Mostrar el formulario)
    else:
        form = AnalisisUploadForm()
        
    return render(request, 'buildings/escanear.html', {'form': form})
def page2(request):
    return render(request, 'buildings/page2.html')

def subir_analisis(request):
    if request.method == 'POST':
        form = AnalisisUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_subido = request.FILES['archivo_analisis']
            nombre_paciente = form.cleaned_data['nombre_paciente']
            
            # 1. Guardar archivo temporalmente
            # Es necesario guardar el archivo en disco para que Tesseract y pdfminer lo lean.
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_analisis', archivo_subido.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, 'wb+') as destination:
                for chunk in archivo_subido.chunks():
                    destination.write(chunk)

            # 2. PROCESAMIENTO HÍBRIDO
            
            # Intento 1: Extracción de texto digital (más limpio y rápido)
            texto_extraido = extraer_texto_de_pdf(temp_path)

            # Intento 2: Si la extracción falla o el archivo no es PDF, usamos OCR
            if not texto_extraido or len(texto_extraido.strip()) < 50:
                print("Usando OCR...")
                texto_extraido = ocr_de_archivo(temp_path)
            
            # 3. ANALIZAR Y GUARDAR
            if texto_extraido:
                resultados = analizar_hemograma(texto_extraido)
                
                # Crear el registro en la base de datos (table1)
                ResultadoPaciente.objects.create(
                    nombre_paciente=nombre_paciente,
                    fecha_analisis=timezone.now().date(), # Usar la fecha actual
                    hb_resultado=resultados.get('hb_resultado'),
                    wbc_resultado=resultados.get('wbc_resultado'),
                    plt_resultado=resultados.get('plt_resultado')
                )
                
                # Opcional: Eliminar archivo temporal
                os.remove(temp_path)
                
                return redirect('analisis_exitoso') # Redirigir a una página de éxito
            else:
                form.add_error('archivo_analisis', 'No se pudo extraer texto del archivo.')

    else:
        form = AnalisisUploadForm()
        
    return render(request, 'buildings/upload_form.html', {'form': form})



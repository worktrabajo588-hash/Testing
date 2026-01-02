from flask import Flask, request
from pdfminer.high_level import extract_text
import io
import re

app = Flask(__name__)

# --- 1. FUNCIÓN DE ANÁLISIS (La lógica del Medilector) ---
def analizar_medico(texto):
    datos = {
        "fecha": "No encontrada",
        "medicamentos": [],
    }
    
    # Buscar fechas (formato DD/MM/AAAA o DD-MM-AAAA)
    fecha_encontrada = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', texto)
    if fecha_encontrada:
        datos["fecha"] = fecha_encontrada.group(1)

    # Lista de ejemplo para detectar medicamentos (puedes ampliarla)
    catalogo = ["Paracetamol", "Ibuprofeno", "Amoxicilina", "Metformina", "Aspirina", "Omeprazol"]
    
    for farmaco in catalogo:
        if farmaco.lower() in texto.lower():
            datos["medicamentos"].append(farmaco)
            
    return datos

# --- 2. RUTA PRINCIPAL (La interfaz y el proceso) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    html_resultados = ""
    
    if request.method == 'POST':
        archivo = request.files['file']
        if archivo:
            # Extraer texto del PDF
            stream = io.BytesIO(archivo.read())
            texto_extraido = extract_text(stream)
            
            # Analizar el texto extraído
            resultados = analizar_medico(texto_extraido)
            
            # Crear el bloque de resultados para mostrar en pantalla
            html_resultados = f'''
            <div style="background: #e1f5fe; padding: 20px; border-radius: 10px; margin-top: 20px; font-family: sans-serif;">
                <h2 style="color: #0277bd;">🩺 Resultados del Análisis</h2>
                <p><strong>📅 Fecha detectada:</strong> {resultados['fecha']}</p>
                <p><strong>💊 Medicamentos encontrados:</strong> {", ".join(resultados['medicamentos']) if resultados['medicamentos'] else "No se detectaron medicamentos del catálogo."}</p>
                <hr>
                <h3>Texto bruto extraído:</h3>
                <pre style="background: #f5f5f5; padding: 10px; border: 1px solid #ccc; white-space: pre-wrap;">{texto_extraido}</pre>
            </div>
            '''
    
    # Retornar la página completa
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medilector</title>
    </head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px;">
        <h1>🚀 Medilector: Analizador de Recetas</h1>
        <p>Sube un archivo PDF para extraer y analizar la información médica.</p>
        <form method="post" enctype="multipart/form-data" style="border: 2px dashed #ccc; padding: 20px; text-align: center;">
            <input type="file" name="file" accept=".pdf">
            <br><br>
            <input type="submit" value="Analizar Documento" style="background: #0277bd; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px;">
        </form>
        
        {html_resultados}
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
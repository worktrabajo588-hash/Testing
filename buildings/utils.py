# import re
# import os
# from io import BytesIO
# from pdfminer.high_level import extract_text
# from PIL import Image
# import pytesseract

# def extraer_texto_de_pdf(file_path):
#     """Extract text from a PDF file using pdfminer."""
#     try:
#         # pdfminer.six necesita la ruta del archivo, no el objeto file de Django.
#         texto = extract_text(file_path)
#         return texto
#     except Exception:
#         return None
    
# def ocr_de_archivo(file_path):
#     try:
#         texto = pytesseract.image_to_string(Image.open(file_path), lang='spa')
#         return texto
#     except Exception as e:
#         print(f"Error en OCR: {e}")
#         return None
    
# def limpiar_texto(texto):
#     """Limpia el texto extraído eliminando espacios innecesarios y líneas vacías."""
#     if not texto:
#         return ""
#     # Eliminar múltiples espacios y líneas vacías
#     texto = re.sub(r'\s+', ' ', texto)
#     texto = re.sub(r'\n\s*\n', '\n', texto)
#     return texto.strip()        

# def guardar_archivo_temporal(archivo_subido):
#     """Guarda el archivo subido en un archivo temporal y devuelve la ruta."""
#     ruta_temporal = f"/tmp/{archivo_subido.name}"
#     with open(ruta_temporal, 'wb+') as destino:
#         for chunk in archivo_subido.chunks():
#             destino.write(chunk)
#     return ruta_temporal

# # --- Lógica de Parsing (Análisis) ---
# def analizar_hemograma(texto_completo):
#     """Busca patrones de hemograma usando RegEx en el texto."""
#     resultados = {}
#     # Patrones para buscar valores numéricos (adaptar a tu formato)
#     # Busca la palabra clave seguida de un número con o sin decimales

#     patron_hb = re.compile(r'(?:Hemoglobina|HB|Hb)\D*?(\d{1,2}\.?\d{0,2})', re.IGNORECASE)
#     patron_wbc = re.compile(r'(?:Leucocitos|WBC|Globulos\s*Blancos)\D*?(\d{3,5})', re.IGNORECASE)
#     patron_plt = re.compile(r'(?:Plaquetas|PLT)\D*?(\d{4,6})', re.IGNORECASE)

#     # Buscar y convertir
#     if (match := patron_hb.search(texto_completo)):
#         resultados['hb_resultado'] = float(match[1])

#     if (match := patron_wbc.search(texto_completo)):
#         # Si el valor de leucocitos es menor a 1000, puede estar reportado en [10^3/uL]
#         val = float(match[1])
#         resultados['wbc_resultado'] = int(val * 1000) if val < 1000 else int(val) # Ajuste simple

#     if (match := patron_plt.search(texto_completo)):
#         resultados['plt_resultado'] = int(match[1])

#     return resultados
    
    

    
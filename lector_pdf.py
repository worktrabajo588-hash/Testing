import tkinter as tk
from tkinter import filedialog, scrolledtext
from pdfminer.high_level import extract_text

def seleccionar_y_leer():
    ruta = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if ruta:
        texto = extract_text(ruta)
        caja_texto.delete(1.0, tk.END) # Limpiar pantalla
        caja_texto.insert(tk.INSERT, texto) # Mostrar texto

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Visor de Texto PDF")

btn = tk.Button(ventana, text="Abrir PDF", command=seleccionar_y_leer)
btn.pack(pady=10)

caja_texto = scrolledtext.ScrolledText(ventana, width=80, height=20)
caja_texto.pack(padx=10, pady=10)

ventana.mainloop()
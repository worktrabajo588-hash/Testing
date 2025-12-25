def analizar_resultados(datos):
    analisis = []

    RANGOS = {
        'hemoglobina': {'min': 12.0, 'max': 16.0, 'label': 'Hemoglobina'},
        'leucocitos_totales': {'min': 4.5, 'max': 11.0, 'label': 'Leucocitos'},
        'plaquetas': {'min': 150.0, 'max': 450.0, 'label': 'Plaquetas'},
        'globulos_rojos': {'min': 4.2, 'max': 5.4, 'label': 'Glóbulos Rojos'},
    }

    for clave, info in RANGOS.items():
        valor = datos.get(clave, 0)

        estado = "Normal"
        clase = "estado-normal"
        mensaje = "Dentro del rango normal."

        if valor == 0:
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
            'valor': valor,
            'estado': estado,
            'mensaje': mensaje,
            'clase': clase
        })

    return analisis

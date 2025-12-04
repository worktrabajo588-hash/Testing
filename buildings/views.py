from django.shortcuts import render

def index(request):
    return render(request, 'buildings/index.html')

def building_detail(request, building_id):
    # Lógica para obtener datos del edificio desde la base de datos
    return render(request, 'buildings/detail.html')

def escanear(request):
    return render(request, 'buildings/escanear.html')

def page2(request):
    return render(request, 'buildings/page2.html')


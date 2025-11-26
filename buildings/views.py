from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'buildings/index.html')

def building_detail(request, building_id):
    # Lógica para obtener datos del edificio desde la base de datos
    return render(request, 'buildings/detail.html')
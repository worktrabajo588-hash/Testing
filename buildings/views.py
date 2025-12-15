
from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, 'buildings/index.html')

def building_detail(request, building_id):
    return render(request, 'buildings/detail.html')

def escanear(request):
    return render(request, 'buildings/escanear.html')

def page2(request):
    return render(request, 'buildings/page2.html')



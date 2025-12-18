# buildings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rutas de la aplicación 'buildings'
    path('', views.index, name='index'),
    path('escanear/', views.escanear, name='escanear'),
    path('page2/', views.page2, name='page2'),
    path('lector/', views.lector, name='lector'),
    path('building/<int:building_id>/', views.building_detail, name='building_detail'),
]
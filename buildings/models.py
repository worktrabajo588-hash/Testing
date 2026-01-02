from django.db import models
from django.contrib.auth.models import User

class DocumentoHemograma(models.Model):
    archivo = models.FileField(upload_to="hemogramas/“). models")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
class Hemograma(models.Model):
    # DATOS DEL PACIENTE
    nombre_completo = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50)
    genero_sexo = models.CharField(max_length=10)
    edad = models.IntegerField()
    fecha_nacimiento = models.DateField()
    procedencia = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # DATOS DEL EXAMEN
    tipo_examen = models.CharField(max_length=100)
    nro_orden = models.CharField(max_length=50)
    fecha_ingreso = models.DateField()
    
    # SERIE ROJA
    globulos_rojos = models.FloatField()
    hemoglobina = models.FloatField()
    hematocrito = models.FloatField()
    vmc = models.FloatField()
    hcm = models.FloatField()
    chcm = models.FloatField()
    
    # PLAQUETAS
    plaquetas = models.FloatField()
    
    # SERIE BLANCA
    leucocitos_totales = models.FloatField()
    neutrofilos_p = models.FloatField()
    linfocitos_p = models.FloatField()
    monocitos_p = models.FloatField()
    eosinofilos_p = models.FloatField()
    basofilos_p = models.FloatField()
    

    def __str__(self):
        return f"Hemograma de {self.nro_orden} - {self.nombre_completo()}"
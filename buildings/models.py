from django.db import models
from django.contrib.auth.models import User

class Hemograma(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    globulos_rojos = models.FloatField()
    hemoglobina = models.FloatField()
    hematocrito = models.FloatField()
    leucocitos_totales = models.FloatField()
    neutrofilos_p = models.FloatField()
    linfocitos_p = models.FloatField()
    plaquetas = models.FloatField()

    def __str__(self):
        return f"Hemograma de {self.usuario.username} - {self.fecha.date()}"

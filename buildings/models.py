from django.db import models

# Create your models here.
# 1. Tabla de Referencia del Hemograma (Valores Normales)
class HemogramaReferencia(models.Model):
    # Usamos db_table para asegurarnos de que Django use el nombre exacto que le dimos si lo creamos con SQL puro.
    # Si usaste el ORM para crearla, Django la llamará: nombre_app_hemogramareferencia
    
    parametro = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Parámetro del Hemograma"
    )
    valores_normales = models.CharField(
        max_length=200,
        verbose_name="Valores Normales"
    )
    causas_alto = models.TextField(
        blank=True,
        null=True,
        verbose_name="Causas de Valor Alto (↑)"
    )
    causas_bajo = models.TextField(
        blank=True,
        null=True,
        verbose_name="Causas de Valor Bajo (↓)"
    )

    class Meta:
        verbose_name = "Parámetro de Referencia"
        verbose_name_plural = "Parámetros de Referencia"
        # Si usaste un nombre SQL directo, ajusta esto:
        # db_table = 'HEMOGRAMA_COMPLETO' 
        
    def __str__(self):
        return self.parametro
    
# 2. Tabla de Resultados de Pacientes (table1)
class ResultadoPaciente(models.Model):
    nombre_paciente = models.CharField(max_length=150)
    fecha_analisis = models.DateField()
    
    # Resultados (usando null=True para permitir que los campos estén vacíos)
    hb_resultado = models.FloatField(
        verbose_name="Hemoglobina",
        null=True, blank=True
    )
    wbc_resultado = models.IntegerField(
        verbose_name="Leucocitos",
        null=True, blank=True
    )
    plt_resultado = models.IntegerField(
        verbose_name="Plaquetas",
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Resultado del Paciente"
        verbose_name_plural = "Resultados de Pacientes"
        # MUY IMPORTANTE: Si creaste esta tabla directamente con SQL (CREATE TABLE table1...), 
        # DEBES forzar a Django a usar ese nombre de tabla EXACTO.
        db_table = 'table1' 
        
    def __str__(self):
        return f"Resultado de {self.nombre_paciente} del {self.fecha_analisis}"
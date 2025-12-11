from django import forms
from .models import HemogramaReferencia, ResultadoPaciente

# The class `AnalisisUploadForm` defines a form with fields for a patient's name and for uploading a
# PDF or image file.
class AnalisisUploadForm(forms.Form):
    nombre_paciente = forms.CharField(max_length=150, label='Nombre del Paciente')
    archivo_analisis = forms.FileField(label='Subir PDF o Imagen (JPG/PNG)')
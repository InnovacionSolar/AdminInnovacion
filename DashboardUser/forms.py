from .models import Asistencia
from django.forms import ModelForm
from DashboardAdmin.models import Empleado
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django import forms


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['empleado','actividades_valor','logros','hora_salida','evidencia']
        widgets = {
            'actividades_valor': forms.Textarea(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Actividades de valor realizadas en el día', 'required': 'required','rows': 3,'style': 'resize: vertical;'}),
            'logros': forms.TextInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Metas alcanzadas en el día'}),
            'hora_salida': forms.TimeInput(format='%H:%M',attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'type': 'time', 'step': '60' }),
            'evidencia': forms.FileInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }
        
        exclude = ['empleado','responsabilidades', 'presente','hora_marcada','fecha']
        
        labels = {
            'actividades_valor': 'Actividades de valor',
            'logros': 'Logros',
            'hora_salida': 'Hora de salida',
            'evidencia': 'Evidencia',
        }
#--------------------------------------------------
class AsistenciaFormAdmin(ModelForm):
    class Meta:
        model = Asistencia
        fields = ['empleado','actividades_valor','logros','hora_salida','puntuacion','observaciones']
        widgets = {   
            'actividades_valor': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md','placeholder':'Actividades de valor realizadas en el día'}),
            'logros': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md','placeholder':'Metas alcanzadas en el día'}),
            'hora_salida': forms.TimeInput(format='%H:%M',attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', 'type': 'time', 'step': '60'}),
            'puntuacion': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md','placeholder':'Puntuacion'}), # 'type': 'number', 'min': '18', 'max': '100
            'observaciones': forms.Textarea(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md','placeholder':'Observaciones para el empleado'}), # 'type': 'number', 'min': '18', 'max': '100
        }

        exclude = ['empleado','responsabilidades','presente','hora_marcada','fecha','evidencia']
        
        labels = {
            'actividades_valor': 'Actividades de valor',
            'logros': 'Logros',
            'hora_salida': 'Hora de salida',
            'evidencia': 'Evidencia',
        }
        
class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido','correo','edad','telefono','picture','departamento','alias','fondo','frase']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Nombre'}),   
            'apellido': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Apellido'}),
            'correo': forms.EmailInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Email'}),
            'edad': forms.NumberInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Edad'}), # 'type': 'number', 'min': '18', 'max': '100
            'telefono': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Telefono'}),
            'direccion': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Direccion'}),
            'picture': forms.FileInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'departamento': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Departamento'}),
            'alias': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Alias'}),
            'fondo': forms.FileInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'frase': forms.TextInput(attrs={'class': 'border rounded border-gray-400 w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline','placeholder':'Frase'}),
        }
        exclude = ['user']

class FraseForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['frase']
        widgets = {
            'frase': forms.TextInput(attrs={
                'class': 'border rounded border-gray-400 w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Ingresa tu frase favorita...'
            }),
        }
        exclude = ['nombre', 'apellido','correo','edad','telefono','picture','departamento','alias','fondo','user']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'border border-gray-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Contraseña actual'}),
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'border border-gray-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Nueva contraseña'}),
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'border border-gray-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Confirmar nueva contraseña'}),
    )
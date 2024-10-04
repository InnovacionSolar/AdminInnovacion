from .models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from DashboardUser.models import Horario

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['empleado', 'dia_semana', 'hora_inicio', 'hora_salida']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time'}),
        }

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de usuario', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class EmpleadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'fecha_nac' and field_name != 'fecha_inicio' and field_name != 'fecha_fin' and field_name != 'picture' and field_name != 'active':
                field.widget.attrs.update(
                    {'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
        self.fields['cargo'].empty_label = "Seleccione un cargo"
        self.fields['nombre'].label = 'Nombre'
        self.fields['apellido'].label = 'Apellido'
        self.fields['fecha_nac'].label = 'Fecha de Nacimiento'
        self.fields['telefono'].label = 'Teléfono'
        self.fields['correo'].label = 'Correo'
        self.fields['cargo'].label = 'Cargo'
        self.fields['picture'].label = 'Foto de Perfil'
        self.fields['active'].label = 'Activo'

    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'fecha_nac', 'telefono', 'correo', 'cargo', 'picture',
                  'DNI', 'active', 'fecha_inicio', 'departamento']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre', }),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese el apellido'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese el teléfono'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Ingrese el correo electrónico'}),
            'fecha_nac': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Ingrese el departamento'}),
            'DNI': forms.TextInput(attrs={'placeholder': 'Ingrese el DNI'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input h-5 w-5 text-blue-500 border-gray-300 rounded focus:ring-blue-200'}),
        }
        help_texts = {
            'nombre': 'Ingrese el nombre del empleado.',
            'apellido': 'Ingrese el apellido del empleado.',
            'fecha_nac': 'Seleccione la fecha de nacimiento del empleado.',
            'active': 'Marque esta casilla si el empleado está activo.',
        }


class CategoriaInventarioForm(ModelForm):
    class Meta:
        model = CategoriaInventario
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la categoría', 'class': 'border rounded w-full py-2 mt-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria',
                'precio', 'stock', 'picture', 'sucursal', 'local']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'categoria': forms.Select(attrs={'class': ' form-select w-full border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'id': 'categoria_producto'}),
            'precio': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio del producto', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'stock': forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad en stock', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-5'}),
            'picture': forms.FileInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'sucursal': forms.Select(attrs={'class': ' form-select w-full border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'id': 'sucursal_producto'}),
            'local': forms.Select(attrs={'placeholder': 'Ingrese el local del producto', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre',]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del cargo', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class InformeForm(ModelForm):
    class Meta:
        model = Informe
        fields = ['resumen', 'documento', 'categoria']
        widgets = {
            'resumen': forms.Textarea(attrs={'placeholder': 'Ingrese el resumen del informe', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'documento': forms.FileInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'categoria': forms.Select(attrs={'class': ' form-select w-full border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'id': 'categoria_informe'}),
        }


class CategoriaInformeForm(ModelForm):
    class Meta:
        model = Categoria_Informe
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la categoría', 'class': 'border rounded w-full py-2 mt-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class EmpresaForm(ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'logo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la sucursal', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'logo': forms.FileInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class RecursosForm(ModelForm):
    class Meta:
        model = Recurso
        fields = ['nombre', 'descripcion', 'categoria',
                'link', 'documento', 'background']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del recurso', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Ingrese la descripción del recurso', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'categoria': forms.Select(attrs={'class': ' form-select w-full border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'id': 'categoria_recurso'}),
            'link': forms.TextInput(attrs={'placeholder': 'Ingrese el link del recurso', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'documento': forms.FileInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'background': forms.FileInput(attrs={'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }


class RecursoFormCategoria(ModelForm):
    class Meta:
        model = CategoriaRecurso
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la categoría', 'class': 'border rounded w-full py-2 mt-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

from django.forms import Form

class RegistroSalidaForm(ModelForm):
    class Meta:
        model = RegistroSalida
        fields = ['producto', 'cantidad','motivo','ganacias']
        widgets = {
            'producto': forms.Select(attrs={'class': ' form-select w-full border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'id': 'select2'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad de salida', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'motivo': forms.Textarea(attrs={'placeholder': 'Datos del Cliente:\nNombre:\nDNI:\nRUC:\nVenta libre o facturado:', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'ganacias': forms.NumberInput(attrs={'placeholder': 'Ingrese las ganacias', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }
    
class RegistroEntradaForm(ModelForm):
    class Meta:
        model = RegistroEntrada
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': ' form-select w-full border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'id': 'select2'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad de entrada', 'class': 'border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ['mensaje', 'imagen']
        widgets = {
            'mensaje': forms.TextInput(attrs={'placeholder': 'Escriba su mensaje (opcional)', 'class': 'mb-4 border rounded w-full py-2 mt-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'imagen': forms.FileInput(attrs={'class': 'rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

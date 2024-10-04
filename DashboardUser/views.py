from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from DashboardAdmin.models import Empleado, Notificacion
from .forms import AsistenciaForm,EmpleadoForm, CustomPasswordChangeForm, FraseForm
from .models import Asistencia
from django.contrib import messages
from datetime import date
from datetime import datetime,time
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
import os

class EmpleadoLoginView(LoginView):
    template_name = 'login.html' 
    redirect_authenticated_user = True
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        if user.is_staff:
            return redirect('Home')
        elif user.is_superuser:
            return redirect('Home')
        else:
            return redirect('Home_User')

class DashboardUser(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Obtener la última notificación creada
        notificacion = Notificacion.objects.last()
        
        # Verificar si la notificación es de hoy
        hoy = date.today()
        if notificacion and notificacion.fecha_creacion.date() == hoy:
            context = {
                'url': 'Home',
                'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
                'notificacion': notificacion,
            }
        else:
            context = {
                'url': 'Home',
                'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
                'notificacion': None,
            }
        return render(request, 'User/Home.html',context)
    
class ProfileHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        empleado = request.user.empleado
        form = FraseForm(instance=empleado)
        context = {
            'url': 'Profile',
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
            'form': form,
        }
        return render(request, 'User/Profile.html', context)

    def post(self, request, *args, **kwargs):
        empleado = request.user.empleado
        form = FraseForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frase actualizada correctamente.')
            return redirect('Profile')
        else:
            messages.error(request, 'Hubo un error al actualizar la frase.')
        
        context = {
            'url': 'Profile',
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
            'form': form,
        }
        return render(request, 'User/Profile.html', context)
    
class NotasHomeView(TemplateView):
    template_name = 'User/notas/Notas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = 'Notas' 
        return context
    
class EmpleadoUpdateView(LoginRequiredMixin, View):
    def get(self,request, *args,**kwargs):
        empleado = Empleado.objects.get(user=request.user)
        form = EmpleadoForm(instance=empleado)
        try:
            messages = messages.get_messages(request)
        except:
            messages = None
        context = {
            'EmpleadoForm': form,
            'password_form': CustomPasswordChangeForm(user=request.user),
            'url': 'Profile',
            'message': messages,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
        }
        return render(request, 'User/Update.html',context)
    
    def post(self,request,*args,**kwargs):
        if 'passwordchange' in request.POST:
            password_form = CustomPasswordChangeForm(data=request.POST, user=request.user)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Contraseña actualizada con exito')
                return redirect('ProfileUpdate')
            else:
                messages.error(request, 'Error al actualizar contraseña')
                return redirect('ProfileUpdate')
        elif 'infosubmit' in request.POST:
            empleado = Empleado.objects.get(user=request.user)
            form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
            if form.is_valid():
                form.save()
                messages.success(request, 'Informacion actualizada con exito')
                return redirect('ProfileUpdate')
            else:
                messages.error(request, 'Error al actualizar informacion')
                return redirect('ProfileUpdate')

class AsistenciaHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        empleado = request.user.empleado
        message = messages.get_messages(request)
        fecha_actual = date.today()
        asistencias = Asistencia.objects.filter(empleado=Empleado.objects.get(user=request.user),fecha=fecha_actual)
        asistencia_existente = Asistencia.objects.filter(empleado=empleado, fecha=fecha_actual).exists()
        
        try:
            asistencia = Asistencia.objects.get(empleado=empleado, fecha=fecha_actual)            
        except Asistencia.DoesNotExist:
            asistencia = None   
                    
        hora_actual = datetime.now().time()
        hora_max = time(23, 0, 0)

        if hora_actual <= hora_max:
            hora_limite = False
        else:
            hora_limite = True

        if asistencia_existente:
            form = None
        else:
            form = AsistenciaForm()   
        
        if hora_limite:
            hora_limite = False
            formupdate = None
        else:
            hora_limite = True
            formupdate = AsistenciaForm(instance=asistencia) 
            
        context ={
            'url': 'Asistencia',
            'form': form,
            'formupdate': formupdate,
            'asistencias': asistencias,
            'message': message,
            'asistenciaHoy': asistencia_existente ,
            'hora_actual': hora_actual,
            'fecha_actual': fecha_actual,
            'hora_limite': hora_limite,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
        }
        if request.resolver_match.url_name == 'Salida':
            template_name = 'User/asistencias/Salida.html'
        else:
            template_name = 'User/asistencias/Asistencia.html'
        
        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        if 'asistencia_actualizacion' in request.POST:
            try:
                formupdate = AsistenciaForm(request.POST, instance=Asistencia.objects.get(empleado=Empleado.objects.get(user=request.user),fecha=date.today()))
            except:
                formupdate = None
                
            if formupdate.is_valid():
                evidencia = Asistencia.objects.get(empleado=Empleado.objects.get(user=request.user),fecha=date.today()).evidencia
                formupdate.instance.evidencia = evidencia

                formupdate.save()
                messages.success(request, 'Asistencia de hoy actualizada con exito')
                return redirect('Asistencia')
            else:
                messages.error(request, 'Error al actualizar asistencia')
        else:
            pass

        form = AsistenciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.empleado = Empleado.objects.get(user=request.user)
            form.save()
            messages.success(request, 'Asistencia de hoy registrada con exito')
            return redirect('Asistencia')
        else:
            messages.error(request, 'Error al registrar asistencia')
        context ={
            'url': 'Asistencia',
            'form': form,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),

        }
        # Determina la plantilla a renderizar
        if kwargs.get('name') == 'Salida':
            template_name = 'User/asistencias/Salida.html'
        else:
            template_name = 'User/asistencias/Asistencia.html'
        
        return render(request, template_name, context)
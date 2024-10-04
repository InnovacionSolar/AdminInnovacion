from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Empleado, Cargo, Venta, Producto, Informe
from django.views.generic import View
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from .forms import EmpleadoForm, UserRegisterForm, EmpleadoForm, CargoForm, NotificacionForm, HorarioForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from DashboardUser.models import Horario, Empleado
import os  
from django.views import View
from django.views.generic.edit import UpdateView

class HorarioCreateView(View):
    def get(self, request, *args, **kwargs):
        form = HorarioForm()  # Instancia del formulario para agregar horarios
        horarios = Horario.objects.all()  # Obtén todos los horarios
        empleados = Empleado.objects.all()  # Obtener todos los empleados
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

        context = {
            'form': form,
            'horarios': horarios,
            'empleados': empleados,
            'dias_semana': dias_semana,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', '')
        }
        return render(request, 'Horarios/horario.html', context)
    

    def post(self, request, *args, **kwargs):
        if 'crearhorario_submit' in request.POST:
            form = HorarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Horario creado con éxito')
            else:
                messages.error(request, 'Error al crear el horario')
        return redirect('horario')
       
class EmpleadoHorarioView(View):
    def get(self, request, empleado_id, *args, **kwargs):
        empleado = get_object_or_404(Empleado, id=empleado_id)
        horarios = Horario.objects.filter(empleado=empleado)

        context = {
            'empleado': empleado,
            'horarios': horarios,
        }
        return render(request, 'Horarios/DetailHorario.html', context)
    
class HorarioUpdateView(UpdateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'Horarios/update_horario.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Horario actualizado con éxito')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el horario')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('empleado_horarios', kwargs={'empleado_id': self.object.empleado.id})

class HomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for i in range(1, 13):
                total = Venta.objects.filter(
                    date_joined__year=year, date_joined__month=i).aggregate(r=Sum('monto'))['r']
                data.append(float(total) if total is not None else 0)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        mes_actual = datetime.now().month
        empleados = Empleado.objects.all().count()
        cumpleaños_mes = Empleado.objects.filter(fecha_nac__month=mes_actual)
        cantidad_productos = Producto.objects.all().count()
        cantidad_informes = Informe.objects.all().count()
        context = {
            'empleados': empleados,
            'cantidad_informes': cantidad_informes,
            'url': 'Home',
            'cumpleaños_mes': cumpleaños_mes.count(),
            'cumpleaños_mes_lista': cumpleaños_mes,
            'cantidad_productos': cantidad_productos,
            'hora': datetime.now(),
            'graph_sales_year_month': self.get_graph_sales_year_month(),
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),

        }
        return render(request, 'Dashboard/Home.html', context)


class EmpleadoView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')  # Especifica la URL de inicio de sesión
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        empleados = Empleado.objects.all()
        empleados_inactivos = Empleado.objects.filter(user__is_active=False)

        message = messages.get_messages(request)

        context = {
            'empleados': empleados,
            'url': 'Empleados',
            'hora': datetime.now(),
            'cantidad_empleados': empleados.count(),
            'cantidad_empleados_inactivos': empleados_inactivos.count(),
            'message': message,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),

        }
        return render(request, 'Dashboard/Empleados.html', context)


class EmpleadoCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')  # Especifica la URL de inicio de sesión
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        form = EmpleadoForm()
        form_user = UserRegisterForm()
        context = {
            'form': form,
            'url': 'Empleados',
            'sub_url': 'Nuevo Empleado',
            'hora': datetime.now(),
            'form_user': form_user,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),

        }
        return render(request, 'Dashboard/Form.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(request.POST)
        profile_form = EmpleadoForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            if not Empleado.objects.filter(user=user).exists():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            return redirect('Empleados')
        else:
            form = EmpleadoForm(request.POST)
            form_user = UserRegisterForm(request.POST)
            form_error = True
            error = form.errors
            context = {
                'form': form,
                'url': 'Empleados',
                'sub_url': 'Nuevo Empleado',
                'hora': datetime.now(),
                'form_error': form_error,
                'error': error,
                'form_user': form_user,
                'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
            }
            return render(request, 'Dashboard/Form.html', context)


class EmpleadoEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')  # Especifica la URL de inicio de sesión
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        empleado = Empleado.objects.get(id=self.kwargs['pk'])
        form = EmpleadoForm(instance=empleado)
        context = {
            'form': form,
            'url': 'Empleados',
            'sub_url': 'Editar Empleado',
            'hora': datetime.now(),
            'empleado': empleado,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request, 'Dashboard/Form.html', context)

    def post(self, request, *args, **kwargs):
        empleado = Empleado.objects.get(id=self.kwargs['pk'])
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('Empleados')

        else:
            form_error = True
            error = form.errors
            context = {
                'form': form,
                'url': 'Empleados',
                'sub_url': 'Editar Empleado',
                'hora': datetime.now(),
                'empleado': empleado,
                'form_error': form_error,
                'error': error,
                'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
            }
            return render(request, 'Dashboard/Form.html', context)


class CargoView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        cargos = Cargo.objects.all()
        form = CargoForm()
        message = messages.get_messages(request)

        context = {
            'cargos': cargos,
            'url': 'Cargos',
            'form': form,
            'hora': datetime.now(),
            'message': message,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request, 'Dashboard/Cargos.html', context)

    def post(self, request, *args, **kwargs):
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo agregado con exito')
        else:
            messages.error(request, 'Error al agregar el cargo')
        return redirect('Cargos_Home')


class CargoEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        cargo = get_object_or_404(Cargo, id=kwargs['pk'])
        form = CargoForm(instance=cargo)
        message = messages.get_messages(request)

        context = {
            'url': 'Cargos',
            'form': form,
            'message': message,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request, 'Inventario/Edit.html', context)

    def post(self, request, *args, **kwargs):
        cargo = get_object_or_404(Cargo, id=kwargs['pk'])
        form = CargoForm(request.POST, instance=cargo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo actualizado con exito')
        else:
            messages.error(request, 'Error al actualizar el cargo')
        return redirect('Cargos_Home')


class DeleteEmpleadoView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        empleado = Empleado.objects.get(id=self.kwargs['pk'])
        context = {
            'url': 'Empleados',
            'empleado': empleado,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request, 'Dashboard/Delete.html', context)

    def post(self, request, *args, **kwargs):
        empleado = Empleado.objects.get(id=self.kwargs['pk'])
        user = empleado.user
        user.delete()
        empleado.delete()
        return redirect('Empleados')


class CrearNotificacionView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')  # Especifica la URL de inicio de sesión
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        form = NotificacionForm()
        context = {
            'form': form,
            'url': 'DashboardAdmin',
            'sub_url': 'Crear Notificación',
            'hora': datetime.now(),
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request, 'Dashboard/Notification.html', context)

    def post(self, request, *args, **kwargs):
        form = NotificacionForm(request.POST, request.FILES)
        if form.is_valid():
            notificacion = form.save(commit=False)  # Guarda el formulario pero no lo guarda en la base de datos todavia
            notificacion.creado_por = self.request.user  # Asigna el usuario actual como creado_por
            notificacion.save()  # Ahora guarda la notificación en la base de datos

            return redirect('Home')  # Redirige al Home de DashboardUser después de crear la notificación

        context = {
            'form': form,
            'url': 'DashboardAdmin',
            'sub_url': 'Crear Notificación',
            'hora': datetime.now(),
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request, 'Dashboard/Notification.html', context)
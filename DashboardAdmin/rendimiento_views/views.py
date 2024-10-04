from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from DashboardUser.models import Empleado, Asistencia
from datetime import datetime
from django.db.models import Avg


def get_datos_rendimiento():
    asistencias = Asistencia.objects.values('empleado__nombre').annotate(promedio=Avg('puntuacion'))
    datos_rendimiento = {asistencia['empleado__nombre']: [asistencia['promedio']] for asistencia in asistencias}
    return datos_rendimiento


def get_datos_rendimiento_today():
    dia = datetime.now().date()
    asistencias = Asistencia.objects.filter(fecha=dia).values('empleado__nombre').annotate(puntuacion=Avg('puntuacion'))
    datos_rendimiento = [{'name': asistencia['empleado__nombre'], 'data': [asistencia['puntuacion']]} for asistencia in asistencias]
    return datos_rendimiento


class RendimientoViewHome(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='InformePermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request):
        datos_rendimiento = get_datos_rendimiento()

        context = {
            'url': 'Rendimiento',
            'datos_rendimiento': datos_rendimiento,
            'datos_rendimiento_day': get_datos_rendimiento_today()

        }
        return render(request, 'Rendimiento/Rendimiento.html', context)

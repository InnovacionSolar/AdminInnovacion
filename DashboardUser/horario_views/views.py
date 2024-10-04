from django.shortcuts import render
from django.views.generic import View
from datetime import date, timedelta
from DashboardUser.models import Horario, Asistencia
import os

class HorarioHomeView(View):
    def get(self, request, *args, **kwargs):

        horarios = Horario.objects.filter(
            empleado=request.user.empleado).order_by('empleado')
        actividades = Asistencia.objects.filter(empleado=request.user.empleado)

        context = {
            'horarios': horarios,
            'actividades': actividades,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),

        }
        return render(request, 'User/horarios/horarios.html', context)

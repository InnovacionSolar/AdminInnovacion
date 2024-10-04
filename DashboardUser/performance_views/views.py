from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import os
from datetime import date, timedelta
from ..models import Empleado
import json
from ..models import Asistencia

class PerformanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Ordenar de manera descendente las asistencias
        asistencias = Asistencia.objects.filter(empleado=request.user.empleado)

        fecha_actual = date.today()

        start_of_week = fecha_actual - timedelta(days=fecha_actual.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        asistencias_semana_actual = Asistencia.objects.filter(
            empleado=Empleado.objects.get(user=request.user),
            fecha__gte=start_of_week,
            fecha__lte=end_of_week
        )
        
        puntuaciones_semanales = [0] * 6
        
        try:
            for asistencia in asistencias_semana_actual:
                dia_semana = asistencia.fecha.weekday()
                asistencia.calcular_puntuacion()
                asistenciaPuntos = asistencia.puntuacion
                puntuaciones_semanales[dia_semana] = asistenciaPuntos       
                
            puntuaciones_semanales.append(0)
        except Asistencia.DoesNotExist:
            asistencia = None
                       
        context ={
            'url': 'Rendimiento',
            'asistencias': asistencias,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
            'puntuaciones_semanales' : json.dumps(puntuaciones_semanales),
        }
        return render(request, 'User/analitycs/Home.html',context)
    
class DetailActividadView(LoginRequiredMixin,View):
    def get(self,request,*args,id, **kwargs):
        asistencia = Asistencia.objects.get(id=id)
        asistencia.calcular_puntuacion()
        
        context = {
            'asistencia': asistencia,
            'url': 'Rendimiento',
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN',''),
        }
        return render(request, 'User/analitycs/Detail.html', context)
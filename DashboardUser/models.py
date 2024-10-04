from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.timezone import now as datetime_now
from django.db import models
from DashboardAdmin.models import Empleado
from django.urls import reverse
import re  


class Asistencia(models.Model):
    hora_marcada = models.TimeField(auto_now_add=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.now)
    hora_salida = models.TimeField(blank=True, null=True)
    actividades_valor = models.TextField(blank=True, default='')
    logros = models.TextField(blank=True, null=True, default='')
    evidencia = models.ImageField(upload_to='evidencias/', blank=False, null=False)
    puntuacion = models.IntegerField(blank=True, null=True, default=0)
    observaciones = models.TextField(blank=True, null=True, default='')

    def calcular_puntuacion(self):
        actividades_valor = [ x.strip() for x in self.actividades_valor.split(',') if x.strip()]
        logros = [x.strip() for x in self.logros.split(',') if x.strip()]

        # Cada actividad de valor vale 3 puntos
        puntuacion_actividades_valor = len(actividades_valor) * 3
        puntuacion_metas = len(logros) * 5  # Cada meta vale 5 puntos
        puntuacion_total = puntuacion_actividades_valor + puntuacion_metas
        if puntuacion_total > 20:
            self.puntuacion = 20
        else:
            self.puntuacion = puntuacion_total
        self.save()

    def save(self, *args, **kwargs):
        try:
            this = Asistencia.objects.get(id=self.id)
            if this.evidencia != self.evidencia:
                this.evidencia.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Performance_Detail', args=[str(self.id)])

    def __str__(self):
        return f"Asistencia de {self.empleado.nombre} {self.empleado.apellido} el {self.fecha}"

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

class Horario(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=20, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField(default='00:00:00', blank=False, null=False)
    hora_salida = models.TimeField(default='00:00:00', blank=False, null=False)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return f'{self.empleado.nombre} - {self.dia_semana}: {self.hora_inicio}'
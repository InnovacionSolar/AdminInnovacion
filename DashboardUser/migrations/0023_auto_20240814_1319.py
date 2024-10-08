# Generated by Django 3.2.16 on 2024-08-14 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardUser', '0022_remove_asistencia_logros'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='responsabilidades',
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='actividades_valor',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='horario',
            name='hora_inicio',
            field=models.TimeField(default='00:00:00'),
        ),
    ]

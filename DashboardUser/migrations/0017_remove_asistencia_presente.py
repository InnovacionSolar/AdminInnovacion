# Generated by Django 4.0.1 on 2024-03-19 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardUser', '0016_asistencia_puntuacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='presente',
        ),
    ]

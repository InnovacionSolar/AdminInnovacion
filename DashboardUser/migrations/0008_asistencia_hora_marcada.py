# Generated by Django 4.0.1 on 2024-02-23 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardUser', '0007_alter_asistencia_fecha_alter_asistencia_hora_entrada_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='hora_marcada',
            field=models.TimeField(auto_now=True),
        ),
    ]

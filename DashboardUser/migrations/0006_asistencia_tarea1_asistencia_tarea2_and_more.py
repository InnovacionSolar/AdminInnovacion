# Generated by Django 4.0.1 on 2024-02-15 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardUser', '0005_tarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='tarea1',
            field=models.CharField(default=1, max_length=350),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistencia',
            name='tarea2',
            field=models.CharField(default=1, max_length=350),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistencia',
            name='tarea3',
            field=models.CharField(default=1, max_length=350),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistencia',
            name='tarea4',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='tarea5',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.DeleteModel(
            name='Tarea',
        ),
    ]

# Generated by Django 4.0.1 on 2024-01-31 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardAdmin', '0007_categoriarecurso_recurso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurso',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='recurso',
            name='precio',
        ),
    ]

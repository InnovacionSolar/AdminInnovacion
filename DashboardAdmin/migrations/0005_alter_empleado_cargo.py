# Generated by Django 4.0.1 on 2024-01-22 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardAdmin', '0004_alter_empleado_fecha_fin_alter_empleado_fecha_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DashboardAdmin.cargo'),
        ),
    ]

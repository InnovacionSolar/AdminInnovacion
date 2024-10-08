# Generated by Django 4.0.1 on 2024-02-03 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardAdmin', '0011_remove_cargo_descripcion_alter_empleado_correo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria_Informe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Informe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resumen', models.CharField(max_length=250)),
                ('documento', models.FileField(blank=True, null=True, upload_to='informes/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardAdmin.categoria_informe')),
            ],
        ),
    ]

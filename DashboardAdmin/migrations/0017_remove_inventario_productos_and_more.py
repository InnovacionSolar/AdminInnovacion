# Generated by Django 4.0.1 on 2024-03-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardAdmin', '0016_remove_producto_inventarios_producto_inventario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='productos',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='inventario',
        ),
        migrations.AddField(
            model_name='producto',
            name='inventario',
            field=models.ManyToManyField(related_name='productos', to='DashboardAdmin.Empresa'),
        ),
    ]

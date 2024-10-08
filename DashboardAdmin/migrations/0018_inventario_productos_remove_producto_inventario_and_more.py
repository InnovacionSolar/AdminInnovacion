# Generated by Django 4.0.1 on 2024-03-06 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardAdmin', '0017_remove_inventario_productos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='productos',
            field=models.ManyToManyField(related_name='inventarios_relacionados', to='DashboardAdmin.Producto'),
        ),
        migrations.RemoveField(
            model_name='producto',
            name='inventario',
        ),
        migrations.AddField(
            model_name='producto',
            name='inventario',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='DashboardAdmin.empresa'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.1 on 2024-03-08 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardAdmin', '0021_remove_local_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='local',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='DashboardAdmin.local'),
            preserve_default=False,
        ),
    ]

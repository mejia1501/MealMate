# Generated by Django 5.1.4 on 2024-12-31 20:57

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_r', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pickup_Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_start_time', models.TimeField(default=django.utils.timezone.now)),
                ('p_end_time', models.TimeField(default=django.utils.timezone.now)),
                ('active_pickup', models.BooleanField(default=False)),
                ('d_start_time', models.TimeField(default=django.utils.timezone.now)),
                ('d_end_time', models.TimeField(default=django.utils.timezone.now)),
                ('active_delivery', models.BooleanField(default=False)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Reservaciones_config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesas', models.CharField(blank=True, default='1,', max_length=500, null=True)),
                ('active', models.BooleanField(default=False)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Reservaciones_horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesa', models.IntegerField(default=0)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('horas', models.CharField(max_length=288)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
    ]

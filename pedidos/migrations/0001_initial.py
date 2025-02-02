# Generated by Django 5.1.4 on 2024-12-31 20:57

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
            name='PagoNacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedido', models.IntegerField(default=0)),
                ('is_pagomovil', models.BooleanField(default=False)),
                ('banco', models.CharField(max_length=4)),
                ('monto', models.FloatField(default=0)),
                ('ref', models.IntegerField()),
                ('titular', models.CharField(default='', max_length=40)),
                ('telefono', models.CharField(default='', max_length=11)),
                ('is_efectivo', models.BooleanField(default=False)),
                ('id_nro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='PaypalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedido', models.IntegerField()),
                ('monto', models.FloatField()),
                ('ref', models.IntegerField()),
                ('fecha', models.DateTimeField()),
                ('titular', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('id_nro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido_Delivery',
            fields=[
                ('nro_items', models.CharField(max_length=200)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('notas', models.CharField(max_length=500)),
                ('cantidades', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=20)),
                ('identificacion', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=11)),
                ('ubicacion', models.CharField(default='default', max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('monto', models.FloatField(default=0)),
                ('nro', models.AutoField(primary_key=True, serialize=False)),
                ('id_nro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido_Pickup',
            fields=[
                ('nro', models.AutoField(primary_key=True, serialize=False)),
                ('nro_items', models.CharField(max_length=200)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('notas', models.CharField(max_length=500)),
                ('cantidades', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=40)),
                ('identificacion', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=11)),
                ('monto', models.FloatField(default=0)),
                ('ubicacion', models.CharField(default='default', max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('id_nro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='ZelleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedido', models.IntegerField()),
                ('monto', models.FloatField()),
                ('ref', models.IntegerField()),
                ('fecha', models.DateTimeField()),
                ('titular', models.CharField(max_length=40)),
                ('telefono', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('id_nro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_r.restaurante')),
            ],
        ),
    ]

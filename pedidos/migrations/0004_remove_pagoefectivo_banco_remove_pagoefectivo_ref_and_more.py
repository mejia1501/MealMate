# Generated by Django 5.1.4 on 2025-01-04 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_pagoefectivo_pagomovil_delete_pagonacional'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagoefectivo',
            name='banco',
        ),
        migrations.RemoveField(
            model_name='pagoefectivo',
            name='ref',
        ),
        migrations.RemoveField(
            model_name='pagoefectivo',
            name='telefono',
        ),
        migrations.RemoveField(
            model_name='pagoefectivo',
            name='titular',
        ),
        migrations.AddField(
            model_name='pagoefectivo',
            name='billetes',
            field=models.CharField(default='', max_length=12),
        ),
    ]

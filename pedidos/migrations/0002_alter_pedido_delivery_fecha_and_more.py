# Generated by Django 5.1.4 on 2025-01-03 01:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido_delivery',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pedido_pickup',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

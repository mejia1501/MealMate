# Generated by Django 5.1.4 on 2025-01-05 22:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0004_reservacion_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservacion_cliente',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-05 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_reservaciones_horario_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservaciones_horario',
            name='status',
            field=models.CharField(default='', max_length=144),
        ),
    ]

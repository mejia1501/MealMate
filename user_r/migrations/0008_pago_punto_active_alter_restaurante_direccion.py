# Generated by Django 5.1.4 on 2025-01-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_r', '0007_alter_restaurante_fundacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='punto_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='direccion',
            field=models.CharField(default='', max_length=50),
        ),
    ]

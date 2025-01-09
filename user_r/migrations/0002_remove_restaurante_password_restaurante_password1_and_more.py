# Generated by Django 5.1.4 on 2025-01-07 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_r', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurante',
            name='password',
        ),
        migrations.AddField(
            model_name='restaurante',
            name='password1',
            field=models.CharField(default='', max_length=18),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='password2',
            field=models.CharField(default='', max_length=18),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='username',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='direccion',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='nombre',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='rif',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='telefono',
            field=models.CharField(default='', max_length=11),
        ),
    ]

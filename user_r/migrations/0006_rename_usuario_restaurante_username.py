# Generated by Django 5.1.4 on 2025-01-07 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_r', '0005_rename_username_restaurante_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurante',
            old_name='usuario',
            new_name='username',
        ),
    ]

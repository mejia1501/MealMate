# Generated by Django 5.1.4 on 2025-01-07 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_r', '0004_rename_username_field_restaurante_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurante',
            old_name='username',
            new_name='usuario',
        ),
    ]

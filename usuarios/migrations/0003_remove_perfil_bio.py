# Generated by Django 5.2.3 on 2025-07-11 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_perfil_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='bio',
        ),
    ]

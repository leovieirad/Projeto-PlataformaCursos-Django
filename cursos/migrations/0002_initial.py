# Generated by Django 5.2.3 on 2025-07-08 16:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cursos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='aulaassistida',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='cursos.curso'),
        ),
        migrations.AddField(
            model_name='aula',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aulas', to='cursos.curso'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas', to='cursos.curso'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='aulaassistida',
            unique_together={('usuario', 'aula')},
        ),
        migrations.AlterUniqueTogether(
            name='matricula',
            unique_together={('usuario', 'curso')},
        ),
    ]

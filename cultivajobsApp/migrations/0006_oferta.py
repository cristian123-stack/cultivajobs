# Generated by Django 5.0.1 on 2024-11-12 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cultivajobsApp', '0005_empleador_user_estudiante_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
    ]

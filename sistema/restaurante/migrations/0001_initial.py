# Generated by Django 5.1.6 on 2025-02-23 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='restaurante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('platillo', models.CharField(max_length=100, verbose_name='Título')),
                ('imagen', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('descripcion', models.TextField(null=True, verbose_name='Descripción')),
            ],
        ),
    ]

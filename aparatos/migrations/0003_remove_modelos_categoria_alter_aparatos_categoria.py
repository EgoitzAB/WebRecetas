# Generated by Django 5.0.1 on 2024-04-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparatos', '0002_rename_categorias_aparatos_categoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelos',
            name='categoria',
        ),
        migrations.AlterField(
            model_name='aparatos',
            name='categoria',
            field=models.ManyToManyField(blank=True, to='aparatos.categoria'),
        ),
    ]

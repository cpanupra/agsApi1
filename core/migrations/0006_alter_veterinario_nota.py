# Generated by Django 4.0.4 on 2022-06-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_veterinario_apellidos_alter_veterinario_cmpv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinario',
            name='nota',
            field=models.CharField(max_length=5000),
        ),
    ]

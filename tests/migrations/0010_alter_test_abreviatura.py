# Generated by Django 5.0.7 on 2024-08-12 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_tipotest_rename_selectiontype_tiposeleccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='abreviatura',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

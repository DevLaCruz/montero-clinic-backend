# Generated by Django 5.0.7 on 2024-07-29 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='dni',
            field=models.CharField(default='UNKNOWN', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='terms',
            field=models.BooleanField(default=True),
        ),
    ]

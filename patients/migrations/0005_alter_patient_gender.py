# Generated by Django 5.0.7 on 2024-08-03 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_remove_patient_emergency_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(max_length=1),
        ),
    ]

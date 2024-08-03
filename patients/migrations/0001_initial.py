# Generated by Django 5.0.7 on 2024-07-28 19:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('change_date', models.DateField(auto_now=True)),
                ('change_time', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('department', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('occupation', models.CharField(max_length=255)),
                ('religion', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('education_level', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('legal_guardian', models.CharField(max_length=255)),
                ('guardian_phone', models.CharField(max_length=20)),
                ('relationship', models.CharField(max_length=255)),
                ('emergency_contact', models.CharField(max_length=255)),
                ('emergency_phone', models.CharField(max_length=20)),
                ('is_state', models.BooleanField(default=True)),
                ('benefit', models.CharField(max_length=50)),
                ('change_date', models.DateField(auto_now=True)),
                ('change_time', models.TimeField(auto_now=True)),
                ('id_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patients.company')),
                ('id_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patients.location')),
                ('id_tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dependents', to='patients.patient')),
                ('id_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

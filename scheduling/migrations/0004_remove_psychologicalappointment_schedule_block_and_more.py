# Generated by Django 5.0.7 on 2024-08-21 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('scheduling', '0003_timeslot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='psychologicalappointment',
            name='schedule_block',
        ),
        migrations.RenameField(
            model_name='timeslot',
            old_name='id_time',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='psychologicalappointment',
            name='employee',
        ),
        migrations.AddField(
            model_name='appointmentreason',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='psychologicalappointment',
            name='date',
            field=models.DateField(default='2024-08-21'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('enabled', models.BooleanField(default=True)),
                ('change_date', models.DateField(auto_now_add=True)),
                ('change_time', models.DateTimeField(auto_now_add=True)),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.timeslot')),
            ],
        ),
        migrations.CreateModel(
            name='DaysEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True)),
                ('change_date', models.DateField(auto_now_add=True)),
                ('change_time', models.DateTimeField(auto_now_add=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.day')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
        ),
        migrations.AddField(
            model_name='psychologicalappointment',
            name='days_employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduling.daysemployee'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ScheduleBlock',
        ),
    ]

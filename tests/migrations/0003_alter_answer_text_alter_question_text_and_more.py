# Generated by Django 5.0.7 on 2024-07-28 00:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_userresponse'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_responses', to='tests.question'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='selected_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tests.answer'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL),
        ),
    ]

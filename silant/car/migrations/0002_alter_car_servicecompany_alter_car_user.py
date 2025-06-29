# Generated by Django 5.2.2 on 2025-06-21 07:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='servicecompany',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car', to='car.serviceorg', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='car',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
    ]

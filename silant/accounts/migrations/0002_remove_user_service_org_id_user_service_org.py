# Generated by Django 5.2.2 on 2025-06-21 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('car', '0002_alter_car_servicecompany_alter_car_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='service_org_id',
        ),
        migrations.AddField(
            model_name='user',
            name='service_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car.serviceorg', verbose_name='Сервисная организация'),
        ),
    ]

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('service', 'Сервисная организация'),
        ('manager', 'Менеджер'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name='Роль пользователя'
    )
    service_org = models.ForeignKey(
        'car.Serviceorg',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Сервисная организация'
    )

    @property
    def is_service(self):
        return self.role == 'service' and self.service_org is not None

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_client(self):
        return self.role == 'client'




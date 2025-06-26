from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

import car


class Carmodel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name
class Enginemodel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name

class Transmodel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name

class Axdrivemodel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name

class Axcontrolmodel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name
class Serviceorg(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name


class Car(models.Model):
    carnumber =models.CharField(blank=True, unique=True,  null=False, verbose_name='Зав. № машины')
    carmodel = models.ForeignKey(Carmodel,on_delete=models.SET_NULL, null=True, related_name='carmodels',
                                 verbose_name='Модель техники')
    enginemodel = models.ForeignKey(Enginemodel, on_delete=models.SET_NULL, null=True, related_name='enginemodels',
                                    verbose_name='Модель двигателя')
    enginenumber = models.CharField(blank=True, null=False, verbose_name='Зав. № двигателя')
    transmodel = models.ForeignKey(Transmodel, on_delete=models.SET_NULL, null=True, related_name='transmodels',
                                   verbose_name='Модель трансмиссии')
    transnember = models.CharField(blank=True, null=False, verbose_name='Зав. № трансмиссии')
    axdrivemodel = models.ForeignKey(Axdrivemodel, on_delete=models.SET_NULL, null=True, related_name='axdrivemodels',
                                     verbose_name='Модель ведущего моста')
    axdrivenumber = models.CharField(blank=True, null=False, verbose_name='Зав. № ведущего моста')
    axcontrolmodel =  models.ForeignKey(Axcontrolmodel, on_delete=models.SET_NULL, null=True, related_name='axcontrolmodels',
                                        verbose_name='Модель управляемого моста')
    axcontrolnumber = models.CharField(blank=True, null=False, verbose_name='Зав. № управляемого моста')
    dataconractsupply = models.CharField(blank=True, null=False, verbose_name='Договор поставки №, дата')
    datashipfactory = models.DateTimeField(blank=True,null=True, verbose_name = "Дата отгрузки с завода")
    consignee = models.CharField(blank=True, verbose_name = "Грузополучатель (конечный потребитель)")
    deliveryadd = models.CharField(blank=True, null=False, verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.CharField(blank=True, verbose_name='Комплектация (доп. опции)')
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                related_name='car',  verbose_name='Клиент')
    servicecompany = models.ForeignKey(Serviceorg,  on_delete=models.SET_NULL, null=True,
                                related_name='car', default=None, verbose_name='Сервисная компания')

    def __str__(self):
        return f"{self.carnumber}, {self.carmodel}"
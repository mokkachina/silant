from django.db import models

from car.models import Car, Serviceorg


class Maintenview(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name
class Failnode(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name

class Recoverymethod(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return self.name

class Maintenance(models.Model):
    viewmainten = models.ForeignKey(Maintenview,on_delete=models.SET_NULL, null=True, related_name='maintenviews',
                                 verbose_name='Вид ТО')
    datamainten = models.DateTimeField(verbose_name='Дата проведения ТО')
    workhour = models.IntegerField(verbose_name='Наработка, м/час')
    workordernum = models.TextField(verbose_name='№ заказ-наряда')
    workorderdate = models.DateTimeField(verbose_name='Дата заказ-наряда')
    maintenorg = models.ForeignKey(Serviceorg,on_delete=models.SET_NULL, null=True, related_name='maintenorgs',
                                 verbose_name='Организация, проводившая ТО')
    car = models.ForeignKey("car.Car", on_delete=models.SET_NULL, null=True, related_name='carsmain',
                                 verbose_name='Машина' )
    serviceorg = models.ForeignKey(Serviceorg, on_delete=models.SET_NULL, null=True, related_name='serviceorgs',
                                 verbose_name='Сервисная компания' )
    def __str__(self):
        return f'{self.maintenorg}, {self.viewmainten}'

class Complaints(models.Model):
    databroke = models.DateTimeField(verbose_name='Дата отказа')
    workhour = models.IntegerField(verbose_name='Наработка, м/час')
    failnode = models.ForeignKey(Failnode,on_delete=models.SET_NULL, null=True, related_name='failnodes',
                                 verbose_name='Узел отказа')
    description = models.TextField(verbose_name='Описание отказа')
    recoverymethod = models.ForeignKey(Recoverymethod,on_delete=models.SET_NULL, null=True, related_name='recoverymethods',
                                 verbose_name='Способ восстановления')
    usepart = models.TextField(verbose_name='Используемые запасные части')
    datamainten = models.DateTimeField(verbose_name='Дата проведения ТО')
    restoredate = models.DateTimeField(verbose_name='Дата восстановления')
    downtime = models.DurationField(blank=True, null=True, verbose_name='Время простоя техники')
    car =  models.ForeignKey(Car,on_delete=models.CASCADE, null=True, related_name='carcom',
                                 verbose_name='Mашина')
    serviceorg = models.ForeignKey(Serviceorg, on_delete=models.SET_NULL, null=True, related_name='servicecom',
                                   verbose_name='Сервисная компания')

    def __str__(self):
        return self.description
    def save(self, *args, **kwargs):
        if self.restoredate and self.databroke:
            self.downtime = self.restoredate- self.databroke
        super().save(*args, **kwargs)
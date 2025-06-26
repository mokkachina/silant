from django.contrib import admin

from car.models import Car, Carmodel, Enginemodel, Transmodel, Axdrivemodel, Axcontrolmodel, Serviceorg

admin.site.register(Car)
admin.site.register(Carmodel)
admin.site.register(Enginemodel)
admin.site.register(Transmodel)
admin.site.register(Axdrivemodel)
admin.site.register(Axcontrolmodel)
admin.site.register(Serviceorg)
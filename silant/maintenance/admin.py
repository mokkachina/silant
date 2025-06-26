from django.contrib import admin

from maintenance.models import Maintenance, Maintenview, Failnode, Recoverymethod, Complaints

admin.site.register(Maintenance)
admin.site.register(Maintenview)
admin.site.register(Failnode)
admin.site.register(Recoverymethod)
admin.site.register(Complaints)
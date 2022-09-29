from django.contrib import admin
#rom django.contrib.auth.admin import UserAdmin
from .models import Sampledatamodel, unitcost, address, addresstable
#from djangoREST.restProject.restApp import models

# Register your models here.

admin.site.register(Sampledatamodel)
admin.site.register(unitcost)
admin.site.register(address)
admin.site.register(addresstable)

#admin.site.register(models.User, UserAdmin)


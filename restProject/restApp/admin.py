from django.contrib import admin
# rom django.contrib.auth.admin import UserAdmin
from .models import *
# from djangoREST.restProject.restApp import models

# Register your models here.

admin.site.register(Sampledatamodel)
admin.site.register(unitcost)
admin.site.register(address)
admin.site.register(addresstable)


admin.site.register(baseRateMultipliers)
admin.site.register(distToCoastMultipliers)
admin.site.register(distToLakeMultipliers)
admin.site.register(distToOceanMultipliers)
admin.site.register(distToRiverMultipliers)
admin.site.register(drainageAreaMultipliers)
admin.site.register(elevation)
admin.site.register(elevRelToLake)
admin.site.register(elevRelToRiver)
admin.site.register(leveeQuality)
admin.site.register(structuralRelElevation)
admin.site.register(territory)

admin.site.register(typeOfUSe)
admin.site.register(foundationType)
admin.site.register(floorsOfInterest)

admin.site.register(riskrating2results)

# admin.site.register(models.User, UserAdmin)

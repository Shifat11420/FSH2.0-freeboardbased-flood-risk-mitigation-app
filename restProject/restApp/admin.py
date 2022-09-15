from django.contrib import admin
#rom django.contrib.auth.admin import UserAdmin
from .models import Sampledatamodel, testmodel
#from djangoREST.restProject.restApp import models

# Register your models here.

admin.site.register(Sampledatamodel)
admin.site.register(testmodel)
#admin.site.register(models.User, UserAdmin)


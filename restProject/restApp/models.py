from asyncio.windows_events import NULL
import datetime
from email.policy import default
from django.db import models

class Sampledatamodel(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    data = models.DateField(default=datetime.date.today)
   
    def __str__(self):
        return self.name

class unitcost(models.Model):
    zipCode = models.CharField(max_length=10, primary_key = True)
    constructionCost = models.FloatField()
    movingCost = models.FloatField()
    lodgingRate = models.FloatField()

    def __str__(self):
        return str(self.zipCode)

class address(models.Model):
    zipCode = models.CharField(max_length=10, default=NULL)
    streetNum = models.IntegerField()
    streetName = models.CharField(max_length=60)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    parishId = models.IntegerField()
    firstFloorHeight = models.FloatField()
    floodLocation = models.FloatField()
    floodScale = models.FloatField()

    def __str__(self):
        return str(self.streetNum)+" "+str(self.streetName)+", "+str(self.city)  +", "+str(self.zipCode)        

class addresstable(models.Model):
    unitCost = models.ForeignKey(unitcost, on_delete = models.SET_NULL, null = True)
    #zipCode = models.CharField(max_length=10, default=NULL)
    streetNum = models.IntegerField()
    streetName = models.CharField(max_length=60)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    parishId = models.IntegerField()
    firstFloorHeight = models.FloatField()
    floodLocation = models.FloatField()
    floodScale = models.FloatField()

    def __str__(self):
        return str(self.streetNum)+" "+str(self.streetName)+", "+str(self.city)  #+", "+str(self.zipCode)    
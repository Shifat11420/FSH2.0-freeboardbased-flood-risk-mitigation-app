import datetime
from django.db import models

class Sampledatamodel(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    data = models.DateField(default=datetime.date.today)
   
    def __str__(self):
        return self.name

class testmodel(models.Model):
    zipCode = models.IntegerField()
    constructionCost = models.FloatField()
    movingCost = models.FloatField()
    lodgingRate = models.FloatField()

    def __str__(self):
        return str(self.zipCode)
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
    zipCode = models.CharField(max_length=10, primary_key=True)
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
        return str(self.streetNum)+" "+str(self.streetName)+", "+str(self.city) + ", "+str(self.zipCode)


class addresstable(models.Model):
    unitCost = models.ForeignKey(
        unitcost, on_delete=models.SET_NULL, null=True)
    # zipCode = models.CharField(max_length=10, default=NULL)
    streetNum = models.IntegerField()
    streetName = models.CharField(max_length=60)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    parishId = models.IntegerField()
    firstFloorHeight = models.FloatField()
    floodLocation = models.FloatField()
    floodScale = models.FloatField()

    def __str__(self):
        # +", "+str(self.zipCode)
        return str(self.streetNum)+" "+str(self.streetName)+", "+str(self.city)


class baseRateMultipliers(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    bi = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    segment = models.IntegerField()
    singleFamilyHomeIndicator = models.CharField(max_length=10)
    ifType = models.CharField(max_length=15)
    ifBuilding = models.FloatField()
    ifContents = models.FloatField()
    ssBuilding = models.FloatField()
    ssContents = models.FloatField()
    tsuBuilding = models.FloatField()
    tsuContents = models.FloatField()
    glBuilding = models.FloatField()
    glContents = models.FloatField()
    ceBuilding = models.FloatField()
    ceContents = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" BI? "+str(self.bi)+" Region? "+str(self.region)+" Segment? "+str(self.segment)


class distToCoastMultipliers(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    bi = models.CharField(max_length=10)
    dtc_meters = models.IntegerField()
    ce = models.FloatField()
    ss = models.FloatField()
    tsu = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" BI? "+str(self.bi)+" Region? "+str(self.region)


class distToLakeMultipliers(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    dtl_meters = models.IntegerField()
    gl = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" DTL(meters)? "+str(self.dtl_meters)


class distToOceanMultipliers(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    bi = models.CharField(max_length=10)
    dto_meters = models.IntegerField()
    ss = models.FloatField()
    tsu = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" BI? "+str(self.bi)+" Region? "+str(self.region)


class distToRiverMultipliers(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    dtr_meters = models.IntegerField()
    ifvalue = models.FloatField()
    ifType = models.CharField(max_length=15)

    def __str__(self):
        return "Levee? "+str(self.levee)+" Region? "+str(self.region)


class drainageAreaMultipliers(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    segment = models.IntegerField()
    da_km2 = models.IntegerField()
    ifvalue = models.FloatField()
    ifType = models.CharField(max_length=15)

    def __str__(self):
        return "Levee? "+str(self.levee)+" Segment? "+str(self.segment)+" Region? "+str(self.region)


class elevation(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    bi = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    elevation_feet = models.IntegerField()
    ifvalue = models.FloatField()
    ifType = models.CharField(max_length=15)
    ss = models.FloatField()
    tsu = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" BI? "+str(self.bi)+" Region? "+str(self.region)


class elevRelToLake(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    erl_feet = models.FloatField()
    gl = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" ERL(feet)? "+str(self.erl_feet)


class elevRelToRiver(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    segment = models.IntegerField()
    riverClass = models.CharField(max_length=20)
    err_feet = models.IntegerField()
    ifvalue = models.FloatField()
    ifType = models.CharField(max_length=15)

    def __str__(self):
        return "Levee? "+str(self.levee)+" Segment? "+str(self.segment)+" Region? "+str(self.region)


class leveeQuality(models.Model):
    id = models.IntegerField(primary_key=True)
    leveeSystemID = models.IntegerField()
    probOfFailPrior = models.FloatField()
    overtoppingReturnPeriod = models.IntegerField()
    leveeQualityFactor = models.FloatField()
    toBeProbOfFailPrior = models.FloatField()
    toBeOvertoppingReturnPeriod = models.IntegerField()
    toBeLeveeQualityFactor = models.FloatField()

    def __str__(self):
        return "Levee SystemID? "+str(self.leveeSystemID)


class structuralRelElevation(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    sre_feet = models.IntegerField()
    ifvalue = models.FloatField()
    ifType = models.CharField(max_length=15)

    def __str__(self):
        return "Levee? "+str(self.levee)+" Region? "+str(self.region)


class territory(models.Model):
    id = models.IntegerField(primary_key=True)
    levee = models.CharField(max_length=10)
    leveeSystemID = models.BigIntegerField()
    bi = models.CharField(max_length=10)
    huc12 = models.FloatField()
    peril = models.CharField(max_length=10)
    ratingFactors = models.FloatField()

    def __str__(self):
        return "Levee? "+str(self.levee)+" Levee SystemID? "+str(self.leveeSystemID)


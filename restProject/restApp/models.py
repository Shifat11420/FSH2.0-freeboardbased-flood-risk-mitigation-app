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

# Baserate- NonLevee


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
        return "Levee- "+str(self.levee)+" BI- "+str(self.bi)+" Region- "+str(self.region)+" Segment- "+str(self.segment)


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


class typeOfUSe(models.Model):
    id = models.IntegerField(primary_key=True)
    typeofuse = models.CharField(max_length=60)
    flood = models.FloatField()
    surge = models.FloatField()
    tsunami = models.FloatField()
    lakes = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)+" Type of use: "+str(self.typeofuse)


class floorsOfInterest(models.Model):
    id = models.IntegerField(primary_key=True)
    homeIndicator = models.CharField(max_length=20)
    ownerIndicator = models.CharField(max_length=20)
    interest = models.CharField(max_length=20)
    allExclCE = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)+" Home indicator: "+str(self.homeIndicator)+" Owner indicator: "+str(self.ownerIndicator)


class foundationType(models.Model):
    id = models.IntegerField(primary_key=True)
    foundationtypes = models.CharField(max_length=60)
    allExclCE = models.FloatField()
    inlandFlood = models.FloatField()
    stormSurge = models.FloatField()
    tsunami = models.FloatField()
    greatLakes = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)+" Foundation types: "+str(self.foundationtypes)


class firstFloorHeight(models.Model):
    id = models.IntegerField(primary_key=True)
    height = models.IntegerField()
    openNoObstructionWFV = models.FloatField()
    openNoObstructionWbyFV = models.FloatField()
    openObstructionWFV = models.FloatField()
    openObstructionWbyFV = models.FloatField()
    closedWallWFV = models.FloatField()
    closedWallWbyFV = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)+" Height: "+str(self.height)


class MEAboveFirstFloor(models.Model):
    id = models.IntegerField(primary_key=True)
    machineryEquipmentAboveFirstFloor = models.CharField(max_length=10)
    coastalErosion = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)


class buildingValue(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.IntegerField()
    allExclCE = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)+" Value: "+str(self.value)


class contentsValue(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.IntegerField()
    allExclCE = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)+" Value: "+str(self.value)


class deductibleITVCovA(models.Model):
    id = models.IntegerField(primary_key=True)
    coverageValueRatio = models.FloatField()
    inlandFlood = models.FloatField()
    SSTsunamiGreatLakesCoastalErosion = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)


class deductibleITVCovC(models.Model):
    id = models.IntegerField(primary_key=True)
    coverageValueRatio = models.FloatField()
    inlandFlood = models.FloatField()
    SSTsunamiGreatLakesCoastalErosion = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)


class deductibleLimitITVCovA(models.Model):
    id = models.IntegerField(primary_key=True)
    coverageValueRatio = models.FloatField()
    inlandFlood = models.FloatField()
    SSTsunamiGreatLakesCoastalErosion = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)


class deductibleLimitITVCovC(models.Model):
    id = models.IntegerField(primary_key=True)
    coverageValueRatio = models.FloatField()
    inlandFlood = models.FloatField()
    SSTsunamiGreatLakesCoastalErosion = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id)


class concentrationRiskMapping(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=30)
    county = models.CharField(max_length=50)
    concentrationRiskTerritory = models.CharField(max_length=10)

    def __str__(self):
        return "Id "+str(self.id)+" State - "+str(self.state)+" County - "+str(self.county)


class concentrationRisk(models.Model):
    id = models.IntegerField(primary_key=True)
    MSA = models.CharField(max_length=10)
    concentrationRiskTerritoryDescription = models.CharField(max_length=100)
    flood = models.FloatField()
    surge = models.FloatField()

    def __str__(self):
        return "Id "+str(self.id) + " MSA - "+str(self.MSA)


# Results Non Levee
class riskrating2results(models.Model):
    id = models.IntegerField(primary_key=True)
    items = models.CharField(max_length=50)
    inlandFloodBuldings = models.FloatField(null=True)
    inlandFloodContents = models.FloatField(null=True)
    stormSurgeBuldings = models.FloatField(null=True)
    stormSurgeContents = models.FloatField(null=True)
    tsunamiBuldings = models.FloatField(null=True)
    tsunamiContents = models.FloatField(null=True)
    greatLakesBuldings = models.FloatField(null=True)
    greatLakesContents = models.FloatField(null=True)
    coastalErosonBuldings = models.FloatField(null=True)
    coastalErosonContents = models.FloatField(null=True)
    allPerilsAllCoverage = models.FloatField(null=True)

    def __str__(self):
        return "Id : "+str(self.id) + " item : "+str(self.items)

# Results Levee


class riskrating2resultsLevee(models.Model):
    id = models.IntegerField(primary_key=True)
    items = models.CharField(max_length=50)
    inlandFloodFluvialBuldings = models.FloatField(null=True)
    inlandFloodFluvialContents = models.FloatField(null=True)
    inlandFloodPluvialBuldings = models.FloatField(null=True)
    inlandFloodPluvialContents = models.FloatField(null=True)
    stormSurgeBuldings = models.FloatField(null=True)
    stormSurgeContents = models.FloatField(null=True)
    tsunamiBuldings = models.FloatField(null=True)
    tsunamiContents = models.FloatField(null=True)
    greatLakesBuldings = models.FloatField(null=True)
    greatLakesContents = models.FloatField(null=True)
    coastalErosonBuldings = models.FloatField(null=True)
    coastalErosonContents = models.FloatField(null=True)
    allPerilsAllCoverage = models.FloatField(null=True)

    def __str__(self):
        return "Id : "+str(self.id) + " item : "+str(self.items)

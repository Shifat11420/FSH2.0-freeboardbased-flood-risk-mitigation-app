from asyncio.windows_events import NULL
import datetime
from email.policy import default
from django.db import models


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

# Risk Rating 2.0 inputs


class homeCondition(models.Model):
    Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Name


class numOfStories(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class mortgage(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class foundationDesigns(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class foundationTypes(models.Model):
    Name = models.CharField(max_length=50)
    foundationDesignforType = models.ForeignKey(
        foundationDesigns, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.Name


class floodInsurance(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class priorClaims(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class federalAssistance(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class investmentType(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class homeShape(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class barrierIslandIndicators(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class singleFamilyHomeIndicator(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class condoUnitOwnerIndicator(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class typeUseID(models.Model):
    Name = models.CharField(max_length=50)
    singleFamilyHomeIndicatorID = models.ForeignKey(
        singleFamilyHomeIndicator, on_delete=models.PROTECT, default=None)
    condoUnitOwnerIndicatorID = models.ForeignKey(
        condoUnitOwnerIndicator, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.Name


class floodVents(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class MandE(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class primaryResidenceIndicator(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name


class userType(models.Model):
    Name = models.CharField(max_length=30)
    primaryResidenceIndicatorID = models.ForeignKey(
        primaryResidenceIndicator, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.Name


class CRSRating(models.Model):
    Name = models.CharField(max_length=30)
    Value = models.FloatField()

    def __str__(self):
        return self.Name


# Risk rating 2.0 datatables
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


class typeOfUse(models.Model):
    id = models.IntegerField(primary_key=True)
    typeofuse = models.CharField(max_length=60)
    flood = models.FloatField(null=True)
    surge = models.FloatField(null=True)
    tsunami = models.FloatField(null=True)
    lakes = models.FloatField(null=True)
    singleFamilyHomeIndicatorID = models.ForeignKey(
        singleFamilyHomeIndicator, on_delete=models.PROTECT, default=None)
    condoUnitOwnerIndicatorID = models.ForeignKey(
        condoUnitOwnerIndicator, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return "Id "+str(self.id)+" Type of use: "+str(self.typeofuse)


class floor(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class floor1to3(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class floor1to100(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class floor1to4(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class stateAbbreviation(models.Model):
    state = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)

    def __str__(self):
        return self.state


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


# Scenaio entity

class scenario(models.Model):
    # id = models.IntegerField(primary_key=True)
    userTypeID = models.ForeignKey(
        userType, on_delete=models.PROTECT, default=None)
    address = models.CharField(null=True, max_length=200)
    typeOfUseID = models.ForeignKey(
        typeUseID, on_delete=models.PROTECT, default=None)
    homeConditionID = models.ForeignKey(
        homeCondition, on_delete=models.PROTECT, default=None)
    livableArea = models.FloatField(null=True)
    firstFloorHeight = models.FloatField(null=True)
    floor1to3ID = models.ForeignKey(
        floor1to3, on_delete=models.PROTECT, default="1")
    floor1to100ID = models.ForeignKey(
        floor1to100, on_delete=models.PROTECT, default="1")
    floor1to4ID = models.ForeignKey(
        floor1to4, on_delete=models.PROTECT, default="1")
    # mortgageID = models.ForeignKey(
    #     mortgage, on_delete=models.PROTECT, default=None)
    foundationTypeID = models.ForeignKey(
        foundationTypes, on_delete=models.PROTECT, default=None)
    # homeShapeID = models.ForeignKey(
    #     homeShape, on_delete=models.PROTECT, default=None)
    # annualFloodRisk = models.FloatField(blank=True, null=True)
    floodInsuranceID = models.ForeignKey(
        floodInsurance, on_delete=models.PROTECT, default=None)
    buildingReplacementValue = models.IntegerField(blank=True, null=True)
    contentsReplacementValue = models.IntegerField(blank=True, null=True)
    buildingCoverage = models.IntegerField(blank=True, null=True)
    contentsCoverage = models.IntegerField(blank=True, null=True)
    buildingDeductible = models.IntegerField(blank=True, null=True)
    contentsDeductible = models.IntegerField(blank=True, null=True)
    priorClaimsID = models.ForeignKey(
        priorClaims, on_delete=models.PROTECT, default=None)
    federalAssistanceID = models.ForeignKey(
        federalAssistance, on_delete=models.PROTECT, default=None)
    investmentTypeID = models.ForeignKey(
        investmentType, on_delete=models.PROTECT, default=None)
    homeEquityLoanInterestRate = models.FloatField(null=True)
    homeEquityLoanPeriod = models.IntegerField(null=True)
    mortgageInterestRate = models.FloatField(null=True)
    mortgagePeriod = models.IntegerField(null=True)
    multiplierVersion = models.IntegerField(null=True)
    userID = models.IntegerField(null=True)
    levee = models.BooleanField(null=True)
    leveeID = models.CharField(null=True, max_length=100)
    leveeQuality = models.FloatField(null=True)
    state = models.CharField(null=True, max_length=10)
    stateLongName = models.CharField(null=True, max_length=50)
    county = models.CharField(null=True, max_length=100)
    fips = models.CharField(null=True, max_length=50)
    segment = models.CharField(null=True, max_length=20)
    concentrationRiskMapping = models.CharField(null=True, max_length=50)
    HUC12 = models.CharField(null=True, max_length=100)
    barrierIslandIndicator = models.ForeignKey(
        barrierIslandIndicators, on_delete=models.PROTECT, default=None)
    baseRatePer1000ofCoverageValue = models.FloatField(null=True)
    MSA = models.CharField(null=True, max_length=50)
    distToRiver = models.FloatField(null=True)
    riverFloodDepth = models.FloatField(null=True)
    riverClass = models.CharField(null=True, max_length=50)
    elevRelToRiver = models.FloatField(null=True)
    drainageArea = models.FloatField(null=True)
    strRelElev = models.FloatField(null=True)
    distToCoast = models.FloatField(null=True)
    distToOcean = models.FloatField(null=True)
    elevation = models.FloatField(null=True)
    distToLake = models.FloatField(null=True)
    elevRelToLake = models.FloatField(null=True)
    floodVentsID = models.ForeignKey(
        floodVents, on_delete=models.PROTECT, default=None)
    MandEID = models.ForeignKey(
        MandE, on_delete=models.PROTECT, default=None)
    crsRating = models.ForeignKey(
        CRSRating, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return "Id : "+str(self.id) + " userTypeID : "+str(self.userTypeID)

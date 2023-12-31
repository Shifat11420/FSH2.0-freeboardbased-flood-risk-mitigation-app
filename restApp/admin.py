from django.contrib import admin
# rom django.contrib.auth.admin import UserAdmin
from .models import *
# from djangoREST.restProject.restApp import models

# Register your models here.

admin.site.register(unitcost)
admin.site.register(address)
admin.site.register(addresstable)


# RR2 inputs
admin.site.register(typeUseID)
admin.site.register(userType)
admin.site.register(homeCondition)
admin.site.register(numOfStories)
admin.site.register(mortgage)
admin.site.register(foundationDesigns)
admin.site.register(floodInsurance)
admin.site.register(federalAssistance)
admin.site.register(priorClaims)
admin.site.register(investmentType)
admin.site.register(homeShape)
admin.site.register(foundationTypes)
admin.site.register(barrierIslandIndicators)
admin.site.register(leveeIndicators)
admin.site.register(singleFamilyHomeIndicator)
admin.site.register(condoUnitOwnerIndicator)
admin.site.register(floodVents)
admin.site.register(MandE)
admin.site.register(primaryResidenceIndicator)
admin.site.register(CRSRating)
admin.site.register(floor)
admin.site.register(floor1to3)
admin.site.register(floor1to100)
admin.site.register(floor1to4)
admin.site.register(stateAbbreviation)

admin.site.register(scenario)

# RR2 datatables
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

admin.site.register(typeOfUse)
admin.site.register(foundationType)
admin.site.register(floorsOfInterest)
admin.site.register(firstFloorHeight)
admin.site.register(MEAboveFirstFloor)
admin.site.register(buildingValue)
admin.site.register(contentsValue)
admin.site.register(deductibleITVCovA)
admin.site.register(deductibleITVCovC)
admin.site.register(deductibleLimitITVCovA)
admin.site.register(deductibleLimitITVCovC)
admin.site.register(concentrationRiskMapping)
admin.site.register(concentrationRisk)


# AAL data
admin.site.register(ddfBuilding)
admin.site.register(ddfContents)
admin.site.register(ddfBuildingNobase1AAE)
admin.site.register(ddfContentsNobase1AAE)
admin.site.register(ddfBuildingNobase2AAE)
admin.site.register(ddfContentsNobase2AAE)
admin.site.register(ddfBuildingWithObsVVE)
admin.site.register(ddfContentsWithObsVVE)
admin.site.register(ddfBuildingWithoutObsVVE)
admin.site.register(ddfContentsWithoutObsVVE)

# RR2 results
admin.site.register(riskrating2results)
admin.site.register(riskrating2resultsLevee)


# admin.site.register(models.User, UserAdmin)

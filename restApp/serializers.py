from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class unitcostSerializer(serializers.ModelSerializer):
    class Meta:
        model = unitcost
        fields = ('zipCode', 'constructionCost', 'movingCost', 'lodgingRate')


class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = address
        fields = ('id', 'zipCode', 'streetNum', 'streetName', 'city', 'zipCode',
                  'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale')


class addresstableSerializer(serializers.ModelSerializer):
    class Meta:
        model = addresstable
        fields = ('id', 'unitCost', 'streetNum', 'streetName', 'city',  'state',
                  'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale')  # 'zipCode',
        depth = 1

#######################


class baserateSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseRateMultipliers
        fields = ('id', 'levee', 'bi', 'region', 'segment', 'singleFamilyHomeIndicator', 'ifType', 'ifBuilding', 'ifContents',
                  'ssBuilding', 'ssContents', 'tsuBuilding', 'tsuContents', 'glBuilding', 'glContents', 'ceBuilding', 'ceContents')


class distToRiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = distToRiverMultipliers
        fields = ('id', 'levee', 'region', 'dtr_meters', 'ifvalue', 'ifType')


class territorySerializer(serializers.ModelSerializer):
    class Meta:
        model = territory
        fields = '__all__'


class riskrating2resultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = riskrating2results
        fields = '__all__'


class riskrating2resultsLeveeSerializer(serializers.ModelSerializer):
    class Meta:
        model = riskrating2resultsLevee
        fields = '__all__'


# Risk Rating 2.0 inputs


class userTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = userType
        fields = '__all__'


class typeUseIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeUseID
        fields = '__all__'


class homeConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = homeCondition
        fields = '__all__'


class numOfStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = numOfStories
        fields = '__all__'


class mortgageSerializer(serializers.ModelSerializer):
    class Meta:
        model = mortgage
        fields = '__all__'


class foundationDesignIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = foundationDesigns
        fields = '__all__'


class foundationTypeIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = foundationTypes
        fields = '__all__'


class floodInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = floodInsurance
        fields = '__all__'


class priorClaimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = priorClaims
        fields = '__all__'


class federalAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = federalAssistance
        fields = '__all__'


class investmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = investmentType
        fields = '__all__'


class homeShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = homeShape
        fields = '__all__'


class barrierIslandIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = barrierIslandIndicators
        fields = '__all__'

class leveeIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = leveeIndicators
        fields = '__all__'

class buildingValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = buildingValue
        fields = '__all__'


class contentsValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = contentsValue
        fields = '__all__'


class scenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = scenario
        fields = '__all__'


class singleFamilyHomeIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = singleFamilyHomeIndicator
        fields = '__all__'


class condoUnitOwnerIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = condoUnitOwnerIndicator
        fields = '__all__'


class floodVentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = floodVents
        fields = '__all__'


class MandESerializer(serializers.ModelSerializer):
    class Meta:
        model = MandE
        fields = '__all__'


class primaryResidenceIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = primaryResidenceIndicator
        fields = '__all__'


class CRSRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRSRating
        fields = '__all__'


class typeOfUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeOfUse
        fields = '__all__'


class floorSerializer(serializers.ModelSerializer):
    class Meta:
        model = floor
        fields = '__all__'


class floor1to3Serializer(serializers.ModelSerializer):
    class Meta:
        model = floor1to3
        fields = '__all__'


class floor1to100Serializer(serializers.ModelSerializer):
    class Meta:
        model = floor1to100
        fields = '__all__'


class floor1to4Serializer(serializers.ModelSerializer):
    class Meta:
        model = floor1to4
        fields = '__all__'

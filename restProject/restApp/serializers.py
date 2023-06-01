from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class unitcostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = unitcost
        fields = ('zipCode', 'constructionCost', 'movingCost', 'lodgingRate')


class addressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = address
        fields = ('id', 'zipCode', 'streetNum', 'streetName', 'city', 'zipCode',
                  'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale')


class addresstableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = addresstable
        fields = ('id', 'unitCost', 'streetNum', 'streetName', 'city',  'state',
                  'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale')  # 'zipCode',
        depth = 1

#######################


class baserateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = baseRateMultipliers
        fields = ('id', 'levee', 'bi', 'region', 'segment', 'singleFamilyHomeIndicator', 'ifType', 'ifBuilding', 'ifContents',
                  'ssBuilding', 'ssContents', 'tsuBuilding', 'tsuContents', 'glBuilding', 'glContents', 'ceBuilding', 'ceContents')


class distToRiverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = distToRiverMultipliers
        fields = ('id', 'levee', 'region', 'dtr_meters', 'ifvalue', 'ifType')


class territorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = territory
        fields = '__all__'


class riskrating2resultsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = riskrating2results
        fields = '__all__'


class riskrating2resultsLeveeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = riskrating2resultsLevee
        fields = '__all__'


# Risk Rating 2.0 inputs


class userTypeIDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = userTypeID
        fields = '__all__'


class typeUseIDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = typeUseID
        fields = '__all__'


class homeConditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = homeCondition
        fields = '__all__'


class numOfStoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = numOfStories
        fields = '__all__'


class mortgageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mortgage
        fields = '__all__'


class foundationDesignIDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = foundationDesignID
        fields = '__all__'

class foundationTypeIDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = foundationTypeID
        fields = '__all__'        


class floodInsuranceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = floodInsurance
        fields = '__all__'


class priorClaimsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = priorClaims
        fields = '__all__'


class federalAssistanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = federalAssistance
        fields = '__all__'


class investmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = investmentType
        fields = '__all__'



class homeShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = homeShape
        fields = '__all__'
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        # fields = '__all__'


class SampledatamodelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sampledatamodel
        fields = ('id', 'name', 'alias')


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

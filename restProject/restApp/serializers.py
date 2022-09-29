from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Sampledatamodel, unitcost, address, addresstable


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        #fields = '__all__'

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
        fields = ('id', 'zipCode', 'streetNum', 'streetName', 'city', 'zipCode', 'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale')          


class addresstableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = addresstable
        fields = ('id', 'unitCost', 'streetNum', 'streetName', 'city',  'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale')    #'zipCode',
        depth = 1              
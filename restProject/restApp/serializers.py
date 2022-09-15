from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Sampledatamodel, testmodel


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

class testmodelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = testmodel
        fields = ('id', 'zipCode', 'constructionCost', 'movingCost', 'lodgingRate')  
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, filters
from restApp.serializers import UserSerializer, GroupSerializer, SampledatamodelSerializer, testmodelSerializer
from .models import Sampledatamodel, testmodel
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class SampledatamodelViewSet(viewsets.ModelViewSet):
    queryset = Sampledatamodel.objects.all().order_by('name')
    serializer_class = SampledatamodelSerializer    

class testmodelViewSet(viewsets.ModelViewSet):
    queryset = testmodel.objects.all().order_by('zipCode')
    serializer_class = testmodelSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'zipCode', 'constructionCost', 'movingCost', 'lodgingRate']
    search_fields = ['id', 'zipCode', 'constructionCost', 'movingCost', 'lodgingRate']
    ordering_fields = ['id', 'zipCode', 'constructionCost', 'movingCost', 'lodgingRate']
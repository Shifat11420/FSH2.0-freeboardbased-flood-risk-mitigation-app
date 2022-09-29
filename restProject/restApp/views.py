from operator import add
from urllib import response
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from restApp import serializers
from rest_framework import viewsets
from rest_framework import permissions, filters
from restApp.serializers import UserSerializer, GroupSerializer, SampledatamodelSerializer, unitcostSerializer, addressSerializer, addresstableSerializer
from .models import Sampledatamodel, unitcost, address, addresstable
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

class unitcostViewSet(viewsets.ModelViewSet):
    queryset = unitcost.objects.all().order_by('zipCode')
    serializer_class = unitcostSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = [ 'zipCode', 'constructionCost', 'movingCost', 'lodgingRate']
    search_fields = ['zipCode', 'constructionCost', 'movingCost', 'lodgingRate']
    ordering_fields = ['zipCode', 'constructionCost', 'movingCost', 'lodgingRate']


class addressViewSet(viewsets.ModelViewSet):
    queryset = address.objects.all().order_by('zipCode')
    serializer_class = addressSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'streetNum', 'streetName', 'city', 'zipCode', 'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']
    search_fields = ['id', 'streetNum', 'streetName', 'city', 'zipCode', 'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']
    ordering_fields = ['id', 'streetNum', 'streetName', 'city', 'zipCode', 'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']    


class addresstableViewSet(viewsets.ModelViewSet):
    queryset = addresstable.objects.all().order_by('id')
    serializer_class = addresstableSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'unitCost', 'streetNum', 'streetName', 'city', 'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale'] #'zipCode',
    search_fields = ['id', 'unitCost', 'streetNum', 'streetName', 'city',  'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']  #'zipCode',
    ordering_fields = ['id', 'unitCost', 'streetNum', 'streetName', 'city',  'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']   #'zipCode',


    def create(self, request, *args, **kwargs):
        address_data = request.data
        new_address = addresstable.objects.create(unitCost= unitcost.objects.get(id=address_data["unitCost"]),
                                                    #zipCode= address_data["zipCode"],
                                                    streetNum= address_data["streetNum"],
                                                    streetName= address_data["streetName"],
                                                    city= address_data["city"],
                                                    state= address_data["state"],
                                                    parishId= address_data["parishId"],
                                                    firstFloorHeight= address_data["firstFloorHeight"],
                                                    floodLocation= address_data["floodLocation"],
                                                    floodScale= address_data["floodScale"])
        new_address.save()
        serializer = addresstableSerializer(new_address)

        return Response(serializer.data)
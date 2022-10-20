from operator import add
from urllib import response
from django.shortcuts import render

from django.contrib.auth.models import User, Group
from restApp import serializers
from rest_framework import viewsets
from rest_framework import permissions, filters
from restApp.serializers import UserSerializer, GroupSerializer, SampledatamodelSerializer, unitcostSerializer, addressSerializer, addresstableSerializer
from .models import Sampledatamodel, unitcost, address, addresstable
from django_filters.rest_framework import DjangoFilterBackend

# for nfip
import os
from restApp.nfip.scripts.nfip_policy_functions import *
path = r'F:\fsh-django-rest-api\restProject\restApp\nfip'    
from rest_framework.views import APIView
from rest_framework.response import Response

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

    def get_queryset(self):
        queryset = addresstable.objects.all().order_by('id')
        return queryset

      



class CalculateNfipAPIView(APIView):
    def get(self, request, format=None):

        # baseNumber = self.request.query_params.get('baseNumber')
        # # nullcheck on baseNumber variable
        # if baseNumber is not None:        
        #     baseNumber = int(baseNumber)                
        #     calculatorResult = baseNumber*baseNumber
        # else:
        #     calculatorResult = "You need to supply a baseNumber parameter."

        #get the inputs
        inputs = {}
        inputs['program'] = 'Regular'
        inputs['flood_zone'] = 'A'
        inputs['Type of EC'] =  'BFE' # for A-zone
        inputs['date_construction'] = 'Post-Firm' #self.request.query_params.get('date_construction')   #  #date_construction=Post-Firm
        #inputs['flood_zone'] = 'V'
        #inputs['date_construction'] =  '1981 Post-Firm' #'1975-81 (Post-Firm)'
        ##Replacement cost ratio = Building coverage to replacement cost
        #inputs['Replacement cost ratio'] = '0.75 or more' #'0.50 to 0.74', 'under 0.50  

        inputs['ocupancy'] = 'Residential'
        inputs['number_floors'] =  self.request.query_params.get('number_floors') #2
        inputs['basement/enclosure'] = 'None'

        if inputs['basement/enclosure'] == 'None':
            if inputs['number_floors'] == 1:
                inputs['contents_location'] = 'Only - Above Ground Level' #'Above Ground Level and Higher Floors'
            else:
                inputs['contents_location'] = 'Above Ground Level and Higher Floors' #'Above Ground Level and Higher Floors'

        inputs['elevation_diff'] = 6
        inputs['floodproofed'] = 'No'

        inputs['building_coverage'] = 140000
        inputs['contents_coverage'] = 70000
        inputs['building_deductible'] = 1250
        inputs['contents_deductible'] = 1250

        inputs['CRS_Rating'] = 10
        inputs['Probation'] = 'No'
        inputs['Primary_residence'] = 'No'

        #Esimate the premium
        total_amount_due = homeowner_policy(path,inputs)
        # total_amount_due = landlord_policy(path, inputs)
        # total_amount_due = tenant_policy(path, inputs)

        print("Homeowner premium = ",total_amount_due)

        return Response(total_amount_due)   


class CalculateRiskAPIViewBody(APIView):
    def get(self, request, format=None):        
        
        #calculatorInputs = request.data        
        
        ## Code to process body
        ## 1. Deserialize into model
        ## 2. Do math
        ## 3. Prepare outputs
        ## 4. Serialize to JSON for output
       
        # calculatorOutputs = calculatorInputs["val1"]*1000/2.5
        
        # Request Body
        # {
        #     "val1": 2.36,
        #     "val2": 3,
        #     "choices1": [1,40,20404],
        #     "nested": {
        #         "subval1": 2,
        #         "subval2": 2
        #     }
        # }

        # a = calculatorInputs["choices1"][1] * 1000 / 2.5
        # b = calculatorInputs["nested"]["subval1"] * 22
        # calculatorOutputs = a * b    
        # return Response({
        #     'calculator inputs': calculatorInputs, 
        #     'a': a,
        #     'b': b,
        #     'calculator outputs': calculatorOutputs
        #     })  
        # 

        inputs = request.data    

        if inputs["basement/enclosure"] == "None":
            if inputs["number_floors"] == 1:
                inputs['contents_location'] = "Only - Above Ground Level" #'Above Ground Level and Higher Floors'
            else:
                inputs["contents_location"] = "Above Ground Level and Higher Floors" #'Above Ground Level and Higher Floors'
 
        total_amount_due = homeowner_policy(path,inputs) 

        return Response({
            "content location" : inputs["contents_location"],
            'calculator inputs': inputs,
            'calculator outputs': total_amount_due,
            })                        
from restApp.serializers import riskrating2resultsSerializer
from restApp.models import riskrating2results
from restApp.serializers import baserateSerializer
from restApp.models import baseRateMultipliers
from restApp.riskrating2functions import *
from restApp.rr2NonLevee import *
from restApp.rr2Levee import *
from restApp.homeEquityLoan.HEL import *
from rest_framework.response import Response
from rest_framework.views import APIView
from operator import add
from urllib import response
from django.shortcuts import render

from django.contrib.auth.models import User, Group
from restApp import serializers
from rest_framework import viewsets
from rest_framework import permissions, filters
from restApp.serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend

# for nfip
import os
from restApp.nfip.scripts.nfip_policy_functions import *
path = r'F:\fsh-django-rest-api\restProject\restApp\nfip'


# imports for risk rating 2


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class SampledatamodelViewSet(viewsets.ModelViewSet):
    queryset = Sampledatamodel.objects.all().order_by('name')
    serializer_class = SampledatamodelSerializer


class unitcostViewSet(viewsets.ModelViewSet):
    queryset = unitcost.objects.all().order_by('zipCode')
    serializer_class = unitcostSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['zipCode', 'constructionCost',
                        'movingCost', 'lodgingRate']
    search_fields = ['zipCode', 'constructionCost',
                     'movingCost', 'lodgingRate']
    ordering_fields = ['zipCode', 'constructionCost',
                       'movingCost', 'lodgingRate']


class addressViewSet(viewsets.ModelViewSet):
    queryset = address.objects.all().order_by('zipCode')
    serializer_class = addressSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'streetNum', 'streetName', 'city', 'zipCode',
                        'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']
    search_fields = ['id', 'streetNum', 'streetName', 'city', 'zipCode',
                     'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']
    ordering_fields = ['id', 'streetNum', 'streetName', 'city', 'zipCode',
                       'state', 'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']


class addresstableViewSet(viewsets.ModelViewSet):
    queryset = addresstable.objects.all().order_by('id')
    serializer_class = addresstableSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'unitCost', 'streetNum', 'streetName', 'city', 'state',
                        'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']  # 'zipCode',
    search_fields = ['id', 'unitCost', 'streetNum', 'streetName', 'city',  'state',
                     'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']  # 'zipCode',
    ordering_fields = ['id', 'unitCost', 'streetNum', 'streetName', 'city',  'state',
                       'parishId', 'firstFloorHeight', 'floodLocation', 'floodScale']  # 'zipCode',

    def create(self, request, *args, **kwargs):
        address_data = request.data
        new_address = addresstable.objects.create(unitCost=unitcost.objects.get(id=address_data["unitCost"]),
                                                  # zipCode= address_data["zipCode"],
                                                  streetNum=address_data["streetNum"],
                                                  streetName=address_data["streetName"],
                                                  city=address_data["city"],
                                                  state=address_data["state"],
                                                  parishId=address_data["parishId"],
                                                  firstFloorHeight=address_data["firstFloorHeight"],
                                                  floodLocation=address_data["floodLocation"],
                                                  floodScale=address_data["floodScale"])
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

        # get the inputs
        inputs = {}
        inputs['program'] = 'Regular'
        inputs['flood_zone'] = 'A'
        inputs['Type of EC'] = 'BFE'  # for A-zone
        # self.request.query_params.get('date_construction')   #  #date_construction=Post-Firm
        inputs['date_construction'] = 'Post-Firm'
        # inputs['flood_zone'] = 'V'
        # inputs['date_construction'] =  '1981 Post-Firm' #'1975-81 (Post-Firm)'
        # Replacement cost ratio = Building coverage to replacement cost
        # inputs['Replacement cost ratio'] = '0.75 or more' #'0.50 to 0.74', 'under 0.50

        inputs['ocupancy'] = 'Residential'
        inputs['number_floors'] = self.request.query_params.get(
            'number_floors')  # 2
        inputs['basement/enclosure'] = 'None'

        if inputs['basement/enclosure'] == 'None':
            if inputs['number_floors'] == 1:
                # 'Above Ground Level and Higher Floors'
                inputs['contents_location'] = 'Only - Above Ground Level'
            else:
                # 'Above Ground Level and Higher Floors'
                inputs['contents_location'] = 'Above Ground Level and Higher Floors'

        inputs['elevation_diff'] = 6
        inputs['floodproofed'] = 'No'

        inputs['building_coverage'] = 140000
        inputs['contents_coverage'] = 70000
        inputs['building_deductible'] = 1250
        inputs['contents_deductible'] = 1250

        inputs['CRS_Rating'] = 10
        inputs['Probation'] = 'No'
        inputs['Primary_residence'] = 'No'

        # Esimate the premium
        total_amount_due = homeowner_policy(path, inputs)
        # total_amount_due = landlord_policy(path, inputs)
        # total_amount_due = tenant_policy(path, inputs)

        print("Homeowner premium = ", total_amount_due)

        return Response(total_amount_due)


class CalculateRiskAPIViewBody(APIView):
    def get(self, request, format=None):

        # calculatorInputs = request.data

        # Code to process body
        # 1. Deserialize into model
        # 2. Do math
        # 3. Prepare outputs
        # 4. Serialize to JSON for output

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
                # 'Above Ground Level and Higher Floors'
                inputs['contents_location'] = "Only - Above Ground Level"
            else:
                # 'Above Ground Level and Higher Floors'
                inputs["contents_location"] = "Above Ground Level and Higher Floors"

        total_amount_due = homeowner_policy(path, inputs)

        return Response({
            "content location": inputs["contents_location"],
            # 'calculator inputs': inputs,
            'calculator outputs': total_amount_due,
        })


class CalculateHELAPIView(APIView):
    def get(self, request, format=None):

        inputs = request.data

        # The inpiuts for the function will come from Users and database
        # inputs for postman
        # {
        #     "home_condition": "New",        # user input
        #     "federal_assistance": "No",     # user input
        #     "investment_type": "Loan",      # user input
        #     "Ce": 150,                      # unit elevation cost ( default from Dr. Arash's dissertation)  ***
        #     "Cc": 110,                      # unit cost of constuction (table)
        #     "fc": 2.3,                      # freeboard cost in %(table)
        #     "down_payment": 20,             # default/ user input
        #     "A": 2000,                      # livable area (user input)
        #     "r": 3,                         # interst rate (user input)
        #     "t": 10                         # mortgage time period
        # }

        # home_equity_results = home_equity_loan (home_condition= "New", federal_assistance= "No", investment_type="Loan", Ce=150, Cc=110, fc=2.3, down_payment=20, A=2000, r=3, t=10)
        home_equity_results = home_equity_loan(inputs)
        return Response({'Home Equity Calculator Results': home_equity_results})


class baserateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = baseRateMultipliers.objects.all()
    serializer_class = baserateSerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'levee', 'bi', 'region',
                        'segment', 'singleFamilyHomeIndicator']
    search_fields = ['id', 'levee', 'bi', 'region',
                     'segment', 'singleFamilyHomeIndicator']
    ordering_fields = ['id', 'levee', 'bi', 'region',
                       'segment', 'singleFamilyHomeIndicator']


class distToRiverViewSet(viewsets.ModelViewSet):
    queryset = distToRiverMultipliers.objects.all()
    serializer_class = distToRiverSerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'levee', 'region', 'ifType']


class territoryViewSet(viewsets.ModelViewSet):
    queryset = territory.objects.all()
    serializer_class = territorySerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'levee', 'leveeSystemID',
                        'huc12', 'peril', 'ratingFactors']


class CalculateRR2APIView(APIView):
    def get(self, request, format=None):

        # inputs = request.data

        # --------------------------
        inputs = {}
        # added variables to inputs
        inputs['State'] = 'MI'
        inputs['State (Long)'] = 'Michigan'
        inputs['County'] = 'Bay County'
        inputs['Levee'] = 'Yes'  # 'NL'
        inputs['Levee System ID'] = '004305000025'  # needed for levee yes case
        inputs['HUC12'] = '010700061401'
        inputs['Barrier island indicator'] = 'No'
        inputs['DTR'] = 420.8
        inputs['ERR'] = 10.2
        inputs['DA'] = 12.6
        inputs['SRE'] = 4.2
        inputs['DTC'] = "N/A"
        inputs['DTO'] = "N/A"
        inputs['Elevation'] = 585.3
        inputs['DTL'] = 48.3
        inputs['ERL'] = 6.2
        inputs['River class'] = 'A'
        # 'Single-Family Home - Frame'
        inputs['Type of Use'] = 'Single-Family Home - Frame'
        inputs['Single family home indicator'] = 'Yes'
        inputs['Condo unit owner indicator'] = 'No'
        inputs['Floor of interest'] = '1-2'
        # 'Elevated without Enclosure, Post, Pile, or Pier'
        # 'Slab'
        inputs['Foundation type'] = 'Slab'
        inputs['First floor height'] = 0.5
        inputs['Foundation design'] = 'Closed, Wall'
        inputs['Flood vents'] = 'No'
        inputs['M&E'] = 'No'
        inputs['Prior claims'] = 0
        inputs['Coverage A value'] = 250000
        inputs['Coverage C value'] = 100000
        inputs['Coverage A limit'] = 250000
        inputs['Coverage C limit'] = 100000
        inputs['Coverage A deductible'] = 1250
        inputs['Coverage C deductible'] = 1250
        inputs['CRS discount'] = 15
        inputs['Reserve fund'] = 1.15
        inputs['Probation surcharge'] = 0
        inputs['Primary residence indicator'] = 'Yes'
        inputs['Federal policy fee'] = 50
        inputs['ICC premium'] = 4

        inputs['Prior Claim Rate'] = 2
        inputs['Loss Constant'] = 130
        inputs['Expense Constant'] = 62.99

        rr2res = []
        if inputs['Levee'] == 'No':
            rr2res = RRFunctionsNonLevee(inputs)
        if inputs['Levee'] == 'Yes':
            rr2res = RRFunctionsLevee(inputs)
        return Response({'Risk rating 2 Calculator Results': rr2res})

        # return Response({'Risk rating 2 Calculator Results': riskrating_2_results})


class riskrating2resultsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = riskrating2results.objects.all()
    serializer_class = riskrating2resultsSerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'items']
    search_fields = ['id', 'items']
    ordering_fields = ['id', 'items']

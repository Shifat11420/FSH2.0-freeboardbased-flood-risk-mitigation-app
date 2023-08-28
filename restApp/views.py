from restApp.aalFunctions import *
from restApp.foundationCostFunctions import *
import random
import pandas as pd
from restApp.serializers import riskrating2resultsSerializer
from restApp.models import riskrating2results
from restApp.serializers import baserateSerializer
from restApp.models import baseRateMultipliers
from restApp.riskrating2functions import *
from restApp.rr2NonLevee import *
from restApp.rr2Levee import *
from restApp.homeEquityLoan.HEL import *
from restApp.homeEquityLoanfunctions import *
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

# nfip imports
import os
from restApp.nfip.scripts.nfip_policy_functions import *
path = r'F:\fsh-django-rest-api\restProject\restApp\nfip'


# AAL imports


# imports for risk rating 2

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


class CalculateFSHAPIView(APIView):
    def calculate_AmortizedCost(self, P, r, n, t):
        A = (P * (r/n)) / (1 - (1 + (r/n)) ** (-n*t))
        return A

    def get(self, request, format=None):

        # user inputs
        inputs = {}  # request.data

        # --------------------------
        # inputs = {}
        # # added variables to inputs
        # inputs['State'] = 'MI'
        # inputs['State (Long)'] = 'Michigan'
        # inputs['County'] = 'Bay County'
        # inputs['Levee'] = 'Yes'  # 'NL'
        # inputs['Levee System ID'] = '004305000025'  # needed for levee yes case
        # inputs['HUC12'] = '010700061401'
        # inputs['Barrier island indicator'] = 'No'
        # inputs['DTR'] = 420.8
        # inputs['ERR'] = 10.2
        # inputs['DA'] = 12.6
        # inputs['SRE'] = 4.2
        # inputs['DTC'] = "N/A"
        # inputs['DTO'] = "N/A"
        # inputs['Elevation'] = 585.3
        # inputs['DTL'] = 48.3
        # inputs['ERL'] = 6.2
        # inputs['River class'] = 'A'
        # inputs['Type of Use'] = 'Single-Family Home - Frame'
        # inputs['Single family home indicator'] = 'Yes'
        # inputs['Condo unit owner indicator'] = 'No'  #
        # inputs['Floor of interest'] = '1-2'  #
        # inputs['Foundation type'] = 'Slab'
        # inputs['First floor height'] = 0.5   #
        # inputs['Foundation design'] = 'Closed, Wall'
        # inputs['Flood vents'] = 'No'          #
        # inputs['M&E'] = 'No'       #
        # inputs['Prior claims'] = 0
        # inputs['Coverage A value'] = 250000  #         building value
        # inputs['Coverage C value'] = 100000   #         contents value
        # inputs['Coverage A limit'] = 250000   #        building coverage
        # inputs['Coverage C limit'] = 100000   #        contents coverage
        # inputs['Coverage A deductible'] = 1250        building deductible
        # inputs['Coverage C deductible'] = 1250        contents deductible
        # inputs['CRS discount'] = 15  #
        # inputs['Reserve fund'] = 1.15  #
        # inputs['Probation surcharge'] = 0   #
        # inputs['Primary residence indicator'] = 'Yes'  #
        # inputs['Federal policy fee'] = 50  #
        # inputs['ICC premium'] = 4  #

        # inputs['Prior Claim Rate'] = 2  #
        # inputs['Loss Constant'] = 130   #
        # inputs['Expense Constant'] = 62.99  #
        # A=building, C=contents   value=total replacement value, limit = coverage, deductible=deductible

        scenariosearch = request.query_params.get('Scenario')

        currentScenario = scenario.objects.get(id=scenariosearch)
        # scenariosearch = inputs["Scenario"]
        # currentScenario = scenario.objects.get(id=scenariosearch)
        print("infofromScenarioId : ", currentScenario)
        firstFloorHeightCurrentScenario = currentScenario.firstFloorHeight
        livableArea = currentScenario.livableArea
        leveeIDall = currentScenario.leveeID
        print("leveeIDall = ", leveeIDall)
        leveeIDList = leveeIDall.split(",")
        print("leveeIDList = ", leveeIDList)
        multipleLeveeDict = {}
        for levee in leveeIDList:
            print("levee = ", levee)
            lQ = leveeQuality.objects.filter(leveeSystemID=str(levee)).all()
            if not lQ:
                continue
            print("lQ = ", lQ)
            lqfactor = str(lQ.values()[0]['leveeQualityFactor'])
            multipleLeveeDict[str(levee)] = lqfactor
        print("multipleLeveeDict = ", multipleLeveeDict)
        lqFactorMax = max(multipleLeveeDict.values())
        leveeIdForMaxFactor = list(multipleLeveeDict.keys(
        ))[list(multipleLeveeDict.values()).index(lqFactorMax)]
        leveeIdForMaxFactor = leveeIdForMaxFactor.strip()
        print("leveeIdForMaxFactor = ", leveeIdForMaxFactor)

        # Risk Rating 2.0 initialization
        inputs['Loss Constant'] = 130  # ok
        inputs['Expense Constant'] = 62.99  # ok
        inputs['ICC premium'] = 4  # ok for now---tables coming
        inputs['Reserve fund'] = 1.15  # ok
        inputs['Probation surcharge'] = 0   # ok for now---tables coming
        inputs['Federal policy fee'] = 50  # ok

        totalSavingsPerMonth = []
        rr2res = []
        listofPremiums = []
        listofFFH = []
        listofFFHint = []
        listofPremiumsMonthly = []
        listofPremiumsSavingsMonthly = []
        premiumsNoRounding = []
        LegacyDict = {}

        # AAL initialization
        aal = {}
        aal['FFH'] = []
        aal['AAL'] = []
        aal['userTypeAAL'] = []
        aal['insurerAAL'] = []
        aal['reduction'] = []
        aal['expectedFloodRiskReductionPerMonth'] = []
        aal['expectedIndirectFloodRiskReductionPerMonth'] = []

        # aal['rentalLoss'] = []
        # aal['displacementCost'] = []
        # aal['movingCost'] = []
        # aal['workingHourLoss'] = []

        seed = 123

        flood_depths = [currentScenario.returnPeriod5Y, currentScenario.returnPeriod10Y, currentScenario.returnPeriod20Y, currentScenario.returnPeriod50Y, currentScenario.returnPeriod75Y,
                        currentScenario.returnPeriod100Y, currentScenario.returnPeriod200Y, currentScenario.returnPeriod250Y, currentScenario.returnPeriod500Y]
        print("flood_depths = ", flood_depths)
        for n in range(len(flood_depths)):
            flood_depths[n] = flood_depths[n] * 0.0328084
        print("flood_depths = ", flood_depths)
        return_periods = [5, 10, 20, 50, 75, 100, 200, 250, 500]

        gumbelScale, gumbelLocation = a_u_pointwise(
            return_periods, flood_depths)

        # unitConstructionCost = 92.47
        unitDisplacementCost = 140
        unitMovingCost = 1.20
        ffh = firstFloorHeightCurrentScenario
        ownerType = str(currentScenario.userTypeID)
        buildingReplacementValue = currentScenario.buildingReplacementValue
        insurance = 'Yes'

        # ddfBldg = ddfBuilding.objects.all()
        # ddfConts = ddfContents.objects.all()

        floodzone = currentScenario.floodZone
        if str(currentScenario.typeOfUseID.singleFamilyHomeIndicatorID) == "Yes" and str(currentScenario.typeOfUseID.condoUnitOwnerIndicatorID) == "No":
            floornumber = currentScenario.floor1to3ID
        elif str(currentScenario.typeOfUseID.singleFamilyHomeIndicatorID) == "No" and str(currentScenario.typeOfUseID.condoUnitOwnerIndicatorID) == "No":
            floornumber = currentScenario.floor1to100ID
        elif str(currentScenario.typeOfUseID.singleFamilyHomeIndicatorID) == "No" and str(currentScenario.typeOfUseID.condoUnitOwnerIndicatorID) == "Yes":
            floornumber = currentScenario.floor1to4ID

        if str(floornumber) == "1" and (str(floodzone) in ["A", "AE", "X", "Unknown"]):
            ddfBldg = ddfBuildingNobase1AAE.objects.all()
            ddfConts = ddfContentsNobase1AAE.objects.all()
        elif str(floornumber) != "1" and (str(floodzone) in ["A", "AE", "X", "Unknown"]):
            ddfBldg = ddfBuildingNobase2AAE.objects.all()
            ddfConts = ddfContentsNobase2AAE.objects.all()
        elif str(floornumber) == "1" and (str(floodzone) in ["V", "VE"]) and str(currentScenario.foundationTypeID.foundationDesignforType) == "Open, No Obstruction":
            ddfBldg = ddfBuildingWithoutObsVVE.objects.all()
            ddfConts = ddfContentsWithoutObsVVE.objects.all()
        elif str(floornumber) != "1" and (str(floodzone) in ["V", "VE"]) and str(currentScenario.foundationTypeID.foundationDesignforType) in ["Open, Obstruction", "Closed, Wall"]:
            ddfBldg = ddfBuildingWithObsVVE.objects.all()
            ddfConts = ddfContentsWithObsVVE.objects.all()

        # Foundation Cost initialization
        h = firstFloorHeightCurrentScenario * 0.3048   # changing unit form feet to meter
        # changing unit for square feet to square meter
        bld_area = livableArea * 0.0929
        homeshape = str(currentScenario.homeShapeID)
        foundationType = str(currentScenario.foundationTypeID)
        costResults = {}
        materialsResults = {}
        foundationCostList = []
        foundationCostIncrease = []
        amortizedCostPerMonth = []

        if foundationType == "Slab":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'aGrading': [], 'vFill': [], 'aInsulation': [],
                           '$aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'vSlab': [], 'lEdge_Beam': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [],
                                'elevation(m)': [], 'aGrading': [], 'vFill': [], 'aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'aInsulation': [], 'vSlab': [], 'lEdgeBeam': []}

        elif foundationType == "Elevated with Enclosure, Not Post, Pile, or Pier" or foundationType == "Crawlspace":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'vFill': [], 'aInsulation': [],
                           'aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'vSlab': [], 'lFooting': [], 'aGrading': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'vFill': [],
                                'aInsulation': [], 'aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'vSlab': [], 'lFooting': [], 'aGrading': []}

        elif foundationType == "Elevated with Enclosure, Post, Pile, or Pier":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'lPier': [], 'aInsulation': [],
                           'aVaporBarrier': [], 'aGravel': [], 'vExcavation': [], 'nPad': [], 'vSlab': [], 'lFooting': [], 'aGrading': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'lPier': [],
                                'aInsulation': [], 'aVaporBarrier': [], 'aGravel': [], 'vExcavation': [], 'nPad': [], 'vSlab': [], 'lfooting': [], 'aGrading': []}

        elif foundationType == "Elevated without Enclosure, Post, Pile, or Pier":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'lPier': [], 'vExcavation': [],
                           'aGrading': [], 'aGravel': [], 'aInsulation': [], 'nPad': [], 'vWood': [], 'aWood': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'lPier': [], 'vExcavation': [],
                                'aGrading': [], 'aGravel': [], 'aInsulation': [], 'nPad': [], 'vWood': [], 'aWood': []}

        # Home Equity Loan initialization
        home_condition = currentScenario.homeConditionID
        federal_assistance = currentScenario.federalAssistanceID
        investment_type = currentScenario.investmentTypeID
        Ce = 150
        Cc = 110
        fc = 2.3
        down_payment = 20
        A = livableArea
        r = 0.03  # home equity interest rate or morgage rate
        t = 10  # home equity loan period or morgage period
        n = 12

        # Calculation
        count = 1
        LegacyResults = []
        for i in range(5):
            # Risk rating 2.0
            if str(currentScenario.levee) == "No":
                print("nonlevee", currentScenario.levee)
                rr2res = RRFunctionsNonLevee(count,
                                             inputs, currentScenario, leveeIdForMaxFactor, firstFloorHeightCurrentScenario+i, listofPremiums, listofFFH, listofFFHint, listofPremiumsMonthly, listofPremiumsSavingsMonthly, premiumsNoRounding, LegacyDict, LegacyResults)
            elif str(currentScenario.levee) == "Yes":
                print("levee", currentScenario.levee)
                rr2res = RRFunctionsLevee(count,
                                          inputs, currentScenario, leveeIdForMaxFactor, firstFloorHeightCurrentScenario+i, listofPremiums, listofFFH, listofFFHint, listofPremiumsMonthly, listofPremiumsSavingsMonthly, premiumsNoRounding, LegacyDict, LegacyResults)

            # AAL
            if ownerType == 'Homeowner':
                floorInterest = ''

                if insurance == 'Yes':
                    coverageValueA = currentScenario.buildingCoverage
                    deductibleValueA = currentScenario.buildingDeductible
                    coverageValueC = currentScenario.contentsCoverage
                    deductibleValueC = currentScenario.contentsDeductible

                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfBldg, insurance, coverageValueA, deductibleValueA)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfConts, insurance, coverageValueC, deductibleValueC)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                else:
                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfBldg, insurance)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfConts, insurance)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                aal['FFH'].append(ffh+i)
                aal['AAL'].append(round(buildingAAL[0] + contentsAAL[0], 0))
                aal['userTypeAAL'].append(
                    round(buildingAAL[1] + contentsAAL[1], 0))
                aal['insurerAAL'].append(
                    round(buildingAAL[2] + contentsAAL[2], 0))

                if insurance == 'Yes':
                    aal['reduction'].append(
                        aal['userTypeAAL'][0]-aal['userTypeAAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                else:
                    aal['reduction'].append(aal['AAL'][0]-aal['AAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                aal['expectedIndirectFloodRiskReductionPerMonth'].append(
                    aal['expectedFloodRiskReductionPerMonth'][-1]*0.5)
                # aal['rentalLoss'].append(round(othersAAL[0], 0))
                # aal['displacementCost'].append(round(othersAAL[1], 0))
                # aal['movingCost'].append(round(othersAAL[2], 0))
                # aal['workingHourLoss'].append(round(othersAAL[3], 0))

            elif ownerType == 'Landlord':
                floorInterest = ''  # cd StopAsyncIteration
                # buildingLossFunction = pd.read_csv("DDF_building.csv")

                if insurance == 'Yes':
                    coverageValueA = currentScenario.buildingCoverage
                    deductibleValueA = currentScenario.buildingDeductible
                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfBldg, insurance, coverageValueA, deductibleValueA)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                else:
                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfBldg, insurance)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                aal['FFH'].append(ffh+i)
                aal['AAL'].append(round(buildingAAL[0], 0))
                aal['userTypeAAL'].append(round(buildingAAL[1], 0))
                aal['insurerAAL'].append(round(buildingAAL[2], 0))
                if insurance == 'Yes':
                    aal['reduction'].append(
                        aal['userTypeAAL'][0]-aal['userTypeAAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                else:
                    aal['reduction'].append(aal['AAL'][0]-aal['AAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                aal['expectedIndirectFloodRiskReductionPerMonth'].append(
                    aal['expectedFloodRiskReductionPerMonth'][-1]*0.5)
                # aal['rentalLoss'].append(round(othersAAL[0], 0))
                # aal['displacementCost'].append(round(othersAAL[1], 0))
                # aal['movingCost'].append(round(othersAAL[2], 0))
                # aal['workingHourLoss'].append(round(othersAAL[3], 0))

            elif ownerType == 'Tenant':
                floorInterest = ''
                # contentsLossFunction = pd.read_csv("DDF_contents.csv")

                if insurance == 'Yes':
                    coverageValueC = currentScenario.contentsCoverage
                    deductibleValueC = currentScenario.contentsDeductible

                    random.seed(seed)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfConts, insurance, coverageValueC, deductibleValueC)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                else:
                    random.seed(seed)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfConts, insurance)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                aal['FFH'].append(ffh+i)
                aal['AAL'].append(round(contentsAAL[0], 0))
                aal['userTypeAAL'].append(round(contentsAAL[1], 0))
                aal['insurerAAL'].append(round(contentsAAL[2], 0))
                if insurance == 'Yes':
                    aal['reduction'].append(
                        aal['userTypeAAL'][0]-aal['userTypeAAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                else:
                    aal['reduction'].append(aal['AAL'][0]-aal['AAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                aal['expectedIndirectFloodRiskReductionPerMonth'].append(
                    aal['expectedFloodRiskReductionPerMonth'][-1]*0.5)
                # aal['rentalLoss'].append(round(othersAAL[0], 0))
                # aal['displacementCost'].append(round(othersAAL[1], 0))
                # aal['movingCost'].append(round(othersAAL[2], 0))
                # aal['workingHourLoss'].append(round(othersAAL[3], 0))

            # Foundation Cost

            if homeshape == "Square":
                aspect_ratio = 1.0
            elif homeshape == "Rectangle":
                aspect_ratio = 1.5
            elif homeshape == "Long":
                aspect_ratio = 2.0

            if foundationType == "Slab":
                FoundationCost, costs, materials = slab_on_fill(
                    bld_area, h+i, aspect_ratio, aspect="True", s=3, a=3, i=0.1, g=0.15, W=0.41, σ=30, t=0.1, D=0.51, h_=0.2)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'aGrading', 'vFill', 'aInsulation',
                                    'aGravel', 'vExcavation', 'aVaporBarrier', 'vSlab', 'lEdgeBeam', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio',
                                        'elevation(m)', 'aGrading', 'vFill', 'aGravel', 'vExcavation', 'aVaporBarrier', 'aInsulation', 'vSlab', 'lEdgeBeam']

            elif foundationType == "Elevated with Enclosure, Not Post, Pile, or Pier" or foundationType == "Crawlspace" or foundationType == "Basement":
                FoundationCost, costs, materials = CS1(
                    bld_area, h+i, aspect_ratio, aspect="True", i=0.1, g=0.15, W=0.41, σ=30, t=0.1, D=0.51, h_=0.2, w=0.2)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'vFill', 'aInsulation',
                                    'aGravel', 'vExcavation', 'aVaporBarrier', 'vSlab', 'lFooting', 'aGrading', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'vFill',
                                        'aInsulation', 'aGravel', 'vExcavation', 'aVaporBarrier', 'vSlab', 'lFooting', 'aGrading']

            elif foundationType == "Elevated with Enclosure, Post, Pile, or Pier":
                FoundationCost, costs, materials = CS2(
                    bld_area, h+i, aspect_ratio, aspect="True", C=0.41, P=0.25, W=0.41, t=0.1, D=0.3, h_=0.2, y=3, w=0.2)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'lPier', 'aInsulation',
                                    'aVaporBarrier', 'aGravel', 'vExcavation', 'nPad', 'vSlab', 'lFooting', 'aGrading', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'lPier',
                                        'aInsulation', 'aVaporBarrier', 'aGravel', 'vExcavation', 'nPad', 'vSlab', 'lFooting', 'aGrading']

            # elif foundationType=="CMU stemwalls with wood frame floor assembly on internal CMU piers":
            #     FoundationCost,costs,materials = CS3(bld_area,h+i,aspect_ratio=1.5,aspect="True",i=0.1,g=0.15,W=0.41,σ=30,t=0.1,D=0.51,h_=0.2,w=0.2)

            #     costs_df = pd.DataFrame(costs)
            #     costs_df.columns = ['Building Area','Aspect ratio','Elevation (m)','w','$_A_Mason','$_L_Pier','$_A_Vapor_Barrier','$_A_Insulation','$_A_Gravel','$_V_Excavation','$_N_Pad','$_V_Wood','$_L_Footing','$_A_Grading','$_A_Wood','Total_Cost']
            #     materials_df = pd.DataFrame(materials)
            #     materials_df.columns = ['Building Area','Aspect ratio','Elevation (m)','w','A_Mason','L_Pier','A_Vapor_Barrier','A_Insulation','A_Gravel','V_Excavation','N_Pad','V_Wood','L_Footing','A_Grading','A_Wood']

            elif foundationType == "Elevated without Enclosure, Post, Pile, or Pier":
                FoundationCost, costs, materials = CS4(bld_area, h+i, aspect_ratio, aspect="True", C=0.41, P=0.25,
                                                       W=0.41, D=0.3, h_=0.6, y=3, beam_spacing=2.44, joist_spacing=0.41, α_g=0.003319, α_j=0.002729)
                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'lPier', 'vExcavation',
                                    'aGrading', 'aGravel', 'aInsulation', 'nPad', 'vWood', 'aWood', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio',
                                        'elevation(m)', 'lPier', 'vExcavation', 'aGrading', 'aGravel', 'aInsulation', 'nPad', 'vWood', 'aWood']

            costs_dict = costs_df.to_dict('list')
            materials_dict = materials_df.to_dict('list')

            for key in costResults:
                costResults[key] += costs_dict.get(key, 'nan')

            for key in materialsResults:
                materialsResults[key] += materials_dict.get(key, 'nan')

            foundationCostList.append(FoundationCost)
            foundationCostIncrease.append(FoundationCost-foundationCostList[0])
            amortizedCostPerMonth.append(round(self.calculate_AmortizedCost(
                foundationCostIncrease[-1], r, n, t), 0))

            print("rr2res[premiumsSavingsMonthly][i] = ",
                  rr2res[4]["premiumsSavingsMonthly"][i])

            totalSavingsPerMonth.append(round(-1*amortizedCostPerMonth[-1]-aal['expectedFloodRiskReductionPerMonth']
                                        [-1]+aal['expectedIndirectFloodRiskReductionPerMonth'][-1]+rr2res[4]["premiumsSavingsMonthly"][i], 0))

        FoundationCostResults = {'foundationCost': foundationCostList,
                                 'foundationCostIncrease': foundationCostIncrease,
                                 'amortizedCostPerMonth': amortizedCostPerMonth}

        # Home Equity Loan
        home_equity_results = home_equity_loan_function(
            home_condition, federal_assistance, investment_type, Ce, Cc, fc, down_payment, A, r, t)
        print('Home Equity Calculator Results = ', home_equity_results)

        # return Response({'Home Equity Calculator Results': home_equity_results})
        print('\n')
        print("Risk Rating 2.0  results= ", rr2res, '\n')
        print("AAL results = ", aal, '\n')
        print("Foundation cost results : ", foundationCostList, '\n')
        print("costResults = ", costResults, '\n')
        print("materialsResults = ", materialsResults, '\n')
        maxTotalSavingsPerMonth = max(totalSavingsPerMonth)
        index = totalSavingsPerMonth.index(maxTotalSavingsPerMonth)
        optimumFFH = rr2res[0]["firstFloorHeight"][index]
        print(maxTotalSavingsPerMonth, index, optimumFFH)

        return Response({'riskRating2Results': rr2res, 'aalResults': aal, 'foundationCostResults': FoundationCostResults, 'homeEquityLoanResults': home_equity_results, 'totalSavingsPerMonth': totalSavingsPerMonth, 'optimumFFH': optimumFFH})


class CalculateFSHLegacyAPIView(APIView):
    def calculate_AmortizedCost(self, P, r, n, t):
        A = (P * (r/n)) / (1 - (1 + (r/n)) ** (-n*t))
        return A

    def get(self, request, format=None):

        # user inputs
        inputs = {}  # request.data

        scenariosearch = request.query_params.get('Scenario')

        currentScenario = scenario.objects.get(id=scenariosearch)

        # scenariosearch = inputs["Scenario"]
        # currentScenario = scenario.objects.get(id=scenariosearch)
        print("infofromScenarioId : ", currentScenario)
        firstFloorHeightCurrentScenario = currentScenario.firstFloorHeight
        livableArea = currentScenario.livableArea
        leveeIDall = currentScenario.leveeID
        print("leveeIDall = ", leveeIDall)
        leveeIDList = leveeIDall.split(",")
        print("leveeIDList = ", leveeIDList)
        multipleLeveeDict = {}
        for levee in leveeIDList:
            print("levee = ", levee)
            lQ = leveeQuality.objects.filter(leveeSystemID=str(levee)).all()
            if not lQ:
                continue
            print("lQ = ", lQ)
            lqfactor = str(lQ.values()[0]['leveeQualityFactor'])
            multipleLeveeDict[str(levee)] = lqfactor
        print("multipleLeveeDict = ", multipleLeveeDict)
        lqFactorMax = max(multipleLeveeDict.values())
        leveeIdForMaxFactor = list(multipleLeveeDict.keys(
        ))[list(multipleLeveeDict.values()).index(lqFactorMax)]
        leveeIdForMaxFactor = leveeIdForMaxFactor.strip()
        print("leveeIdForMaxFactor = ", leveeIdForMaxFactor)

        # Risk Rating 2.0
        inputs['Loss Constant'] = 130  # ok
        inputs['Expense Constant'] = 62.99  # ok
        inputs['ICC premium'] = 4  # ok for now---tables coming
        inputs['Reserve fund'] = 1.15  # ok
        inputs['Probation surcharge'] = 0   # ok for now---tables coming
        inputs['Federal policy fee'] = 50  # ok

        totalSavingsPerMonth = []
        resultsAll = []
        listofPremiums = []
        listofFFH = []
        listofFFHint = []
        listofPremiumsMonthly = []
        listofPremiumsSavingsMonthly = []
        premiumsNoRounding = []
        count = 0
        LegacyResults = []
        LegacyDict = {}

        # AAL
        aal = {}
        aal['FFH'] = []
        aal['AAL'] = []
        aal['userTypeAAL'] = []
        aal['insurerAAL'] = []
        aal['reduction'] = []
        aal['expectedFloodRiskReductionPerMonth'] = []
        aal['expectedIndirectFloodRiskReductionPerMonth'] = []
        # aal['rentalLoss'] = []
        # aal['displacementCost'] = []
        # aal['movingCost'] = []
        # aal['workingHourLoss'] = []
        aalLegacyDict = {}

        seed = 123

        flood_depths = [currentScenario.returnPeriod5Y, currentScenario.returnPeriod10Y, currentScenario.returnPeriod20Y, currentScenario.returnPeriod50Y, currentScenario.returnPeriod75Y,
                        currentScenario.returnPeriod100Y, currentScenario.returnPeriod200Y, currentScenario.returnPeriod250Y, currentScenario.returnPeriod500Y]
        print("flood_depths = ", flood_depths)
        for n in range(len(flood_depths)):
            flood_depths[n] = flood_depths[n] * 0.0328084
        print("flood_depths = ", flood_depths)
        return_periods = [5, 10, 20, 50, 75, 100, 200, 250, 500]

        gumbelScale, gumbelLocation = a_u_pointwise(
            return_periods, flood_depths)

        # unitConstructionCost = 92.47
        unitDisplacementCost = 140
        unitMovingCost = 1.20
        ffh = firstFloorHeightCurrentScenario
        ownerType = str(currentScenario.userTypeID)
        buildingReplacementValue = currentScenario.buildingReplacementValue
        insurance = 'Yes'

        # ddfBldg = ddfBuilding.objects.all()
        # ddfConts = ddfContents.objects.all()

        floodzone = currentScenario.floodZone
        if str(currentScenario.typeOfUseID.singleFamilyHomeIndicatorID) == "Yes" and str(currentScenario.typeOfUseID.condoUnitOwnerIndicatorID) == "No":
            floornumber = currentScenario.floor1to3ID
        elif str(currentScenario.typeOfUseID.singleFamilyHomeIndicatorID) == "No" and str(currentScenario.typeOfUseID.condoUnitOwnerIndicatorID) == "No":
            floornumber = currentScenario.floor1to100ID
        elif str(currentScenario.typeOfUseID.singleFamilyHomeIndicatorID) == "No" and str(currentScenario.typeOfUseID.condoUnitOwnerIndicatorID) == "Yes":
            floornumber = currentScenario.floor1to4ID

        if str(floornumber) == "1" and (str(floodzone) in ["A", "AE", "X", "Unknown"]):
            ddfBldg = ddfBuildingNobase1AAE.objects.all()
            ddfConts = ddfContentsNobase1AAE.objects.all()
        elif str(floornumber) != "1" and (str(floodzone) in ["A", "AE", "X", "Unknown"]):
            ddfBldg = ddfBuildingNobase2AAE.objects.all()
            ddfConts = ddfContentsNobase2AAE.objects.all()
        elif str(floornumber) == "1" and (str(floodzone) in ["V", "VE"]) and str(currentScenario.foundationTypeID.foundationDesignforType) == "Open, No Obstruction":
            ddfBldg = ddfBuildingWithoutObsVVE.objects.all()
            ddfConts = ddfContentsWithoutObsVVE.objects.all()
        elif str(floornumber) != "1" and (str(floodzone) in ["V", "VE"]) and str(currentScenario.foundationTypeID.foundationDesignforType) in ["Open, Obstruction", "Closed, Wall"]:
            ddfBldg = ddfBuildingWithObsVVE.objects.all()
            ddfConts = ddfContentsWithObsVVE.objects.all()

        # Foundation Cost
        h = firstFloorHeightCurrentScenario * 0.3048   # changing unit form feet to meter
        # changing unit for square feet to square meter
        bld_area = livableArea * 0.0929
        homeshape = str(currentScenario.homeShapeID)
        foundationType = str(currentScenario.foundationTypeID)
        costResults = {}
        materialsResults = {}
        foundationCostList = []
        foundationCostIncrease = []
        amortizedCostPerMonth = []

        if foundationType == "Slab":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'aGrading': [], 'vFill': [], 'aInsulation': [],
                           '$aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'vSlab': [], 'lEdge_Beam': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [],
                                'elevation(m)': [], 'aGrading': [], 'vFill': [], 'aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'aInsulation': [], 'vSlab': [], 'lEdgeBeam': []}

        elif foundationType == "Elevated with Enclosure, Not Post, Pile, or Pier" or foundationType == "Crawlspace":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'vFill': [], 'aInsulation': [],
                           'aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'vSlab': [], 'lFooting': [], 'aGrading': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'vFill': [],
                                'aInsulation': [], 'aGravel': [], 'vExcavation': [], 'aVaporBarrier': [], 'vSlab': [], 'lFooting': [], 'aGrading': []}

        elif foundationType == "Elevated with Enclosure, Post, Pile, or Pier":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'lPier': [], 'aInsulation': [],
                           'aVaporBarrier': [], 'aGravel': [], 'vExcavation': [], 'nPad': [], 'vSlab': [], 'lFooting': [], 'aGrading': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'w': [], 'aMason': [], 'lPier': [],
                                'aInsulation': [], 'aVaporBarrier': [], 'aGravel': [], 'vExcavation': [], 'nPad': [], 'vSlab': [], 'lfooting': [], 'aGrading': []}

        elif foundationType == "Elevated without Enclosure, Post, Pile, or Pier":
            costResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'lPier': [], 'vExcavation': [],
                           'aGrading': [], 'aGravel': [], 'aInsulation': [], 'nPad': [], 'vWood': [], 'aWood': [], 'totalCost': []}
            materialsResults = {'buildingArea': [], 'aspectRatio': [], 'elevation(m)': [], 'lPier': [], 'vExcavation': [],
                                'aGrading': [], 'aGravel': [], 'aInsulation': [], 'nPad': [], 'vWood': [], 'aWood': []}

        # Home Equity Loan initialization
        home_condition = currentScenario.homeConditionID
        federal_assistance = currentScenario.federalAssistanceID
        investment_type = currentScenario.investmentTypeID
        Ce = 150
        Cc = 110
        fc = 2.3
        down_payment = 20
        A = livableArea
        r = 0.03  # home equity interest rate or morgage rate
        t = 10  # home equity loan period or morgage period
        n = 12

        # Calculation
        for i in range(5):
            # Risk rating 2.0
            if str(currentScenario.levee) == "No":
                print("nonlevee", currentScenario.levee)
                resultsAll = RRFunctionsNonLevee(count,
                                                 inputs, currentScenario, leveeIdForMaxFactor, firstFloorHeightCurrentScenario+i, listofPremiums, listofFFH, listofFFHint, listofPremiumsMonthly, listofPremiumsSavingsMonthly, premiumsNoRounding, LegacyDict, LegacyResults)
            elif str(currentScenario.levee) == "Yes":
                print("levee", currentScenario.levee)
                resultsAll = RRFunctionsLevee(count,
                                              inputs, currentScenario, leveeIdForMaxFactor, firstFloorHeightCurrentScenario+i, listofPremiums, listofFFH, listofFFHint, listofPremiumsMonthly, listofPremiumsSavingsMonthly, premiumsNoRounding, LegacyDict, LegacyResults)

            # LegacyResults.append(resultsAll)

            # AAL
            if ownerType == 'Homeowner':
                floorInterest = ''

                if insurance == 'Yes':
                    coverageValueA = currentScenario.buildingCoverage
                    deductibleValueA = currentScenario.buildingDeductible
                    coverageValueC = currentScenario.contentsCoverage
                    deductibleValueC = currentScenario.contentsDeductible

                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfBldg, insurance, coverageValueA, deductibleValueA)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfConts, insurance, coverageValueC, deductibleValueC)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                else:
                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfBldg, insurance)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfConts, insurance)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                aal['FFH'].append(ffh+i)
                aal['AAL'].append(round(buildingAAL[0] + contentsAAL[0], 0))
                aal['userTypeAAL'].append(
                    round(buildingAAL[1] + contentsAAL[1], 0))
                aal['insurerAAL'].append(
                    round(buildingAAL[2] + contentsAAL[2], 0))
                if insurance == 'Yes':
                    aal['reduction'].append(
                        aal['userTypeAAL'][0]-aal['userTypeAAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                else:
                    aal['reduction'].append(aal['AAL'][0]-aal['AAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                aal['expectedIndirectFloodRiskReductionPerMonth'].append(
                    aal['expectedFloodRiskReductionPerMonth'][-1]*0.5)
                # aal['rentalLoss'].append(round(othersAAL[0], 0))
                # aal['displacementCost'].append(round(othersAAL[1], 0))
                # aal['movingCost'].append(round(othersAAL[2], 0))
                # aal['workingHourLoss'].append(round(othersAAL[3], 0))

                LegacyDict['AAL'] = aal['AAL'][i]
                LegacyDict['userTypeAAL'] = aal['userTypeAAL'][i]
                LegacyDict['insurerAAL'] = aal['insurerAAL'][i]
                LegacyDict['reduction'] = aal['reduction'][i]
                LegacyDict['expectedFloodRiskReductionPerMonth'] = aal['expectedFloodRiskReductionPerMonth'][i]
                LegacyDict['expectedIndirectFloodRiskReductionPerMonth'] = aal['expectedIndirectFloodRiskReductionPerMonth'][i]

            elif ownerType == 'Landlord':
                floorInterest = ''  # cd StopAsyncIteration
                # buildingLossFunction = pd.read_csv("DDF_building.csv")

                if insurance == 'Yes':
                    coverageValueA = currentScenario.buildingCoverage
                    deductibleValueA = currentScenario.buildingDeductible
                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfBldg, insurance, coverageValueA, deductibleValueA)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                else:
                    random.seed(seed)
                    buildingAAL = aal_building(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfBldg, insurance)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                aal['FFH'].append(ffh+i)
                aal['AAL'].append(round(buildingAAL[0], 0))
                aal['userTypeAAL'].append(round(buildingAAL[1], 0))
                aal['insurerAAL'].append(round(buildingAAL[2], 0))
                if insurance == 'Yes':
                    aal['reduction'].append(
                        aal['userTypeAAL'][0]-aal['userTypeAAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                else:
                    aal['reduction'].append(aal['AAL'][0]-aal['AAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                aal['expectedIndirectFloodRiskReductionPerMonth'].append(
                    aal['expectedFloodRiskReductionPerMonth'][-1]*0.5)
                # aal['rentalLoss'].append(round(othersAAL[0], 0))
                # aal['displacementCost'].append(round(othersAAL[1], 0))
                # aal['movingCost'].append(round(othersAAL[2], 0))
                # aal['workingHourLoss'].append(round(othersAAL[3], 0))
                LegacyDict['AAL'] = aal['AAL'][i]
                LegacyDict['userTypeAAL'] = aal['userTypeAAL'][i]
                LegacyDict['insurerAAL'] = aal['insurerAAL'][i]
                LegacyDict['reduction'] = aal['reduction'][i]
                LegacyDict['expectedFloodRiskReductionPerMonth'] = aal['expectedFloodRiskReductionPerMonth'][i]
                LegacyDict['expectedIndirectFloodRiskReductionPerMonth'] = aal['expectedIndirectFloodRiskReductionPerMonth'][i]

            elif ownerType == 'Tenant':
                floorInterest = ''
                # contentsLossFunction = pd.read_csv("DDF_contents.csv")

                if insurance == 'Yes':
                    coverageValueC = currentScenario.contentsCoverage
                    deductibleValueC = currentScenario.contentsDeductible

                    random.seed(seed)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i, gumbelLocation,
                                               gumbelScale, ddfConts, insurance, coverageValueC, deductibleValueC)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                else:
                    random.seed(seed)
                    contentsAAL = aal_contents(livableArea, buildingReplacementValue, ffh+i,
                                               gumbelLocation, gumbelScale, ddfConts, insurance)
                    othersAAL = aal_others(livableArea, buildingReplacementValue, ffh+i,
                                           gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost)

                aal['FFH'].append(ffh+i)
                aal['AAL'].append(round(contentsAAL[0], 0))
                aal['userTypeAAL'].append(round(contentsAAL[1], 0))
                aal['insurerAAL'].append(round(contentsAAL[2], 0))
                if insurance == 'Yes':
                    aal['reduction'].append(
                        aal['userTypeAAL'][0]-aal['userTypeAAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                else:
                    aal['reduction'].append(aal['AAL'][0]-aal['AAL'][-1])
                    aal['expectedFloodRiskReductionPerMonth'].append(
                        round(aal['reduction'][-1]/12, 4))
                aal['expectedIndirectFloodRiskReductionPerMonth'].append(
                    aal['expectedFloodRiskReductionPerMonth'][-1]*0.5)
                # aal['rentalLoss'].append(round(othersAAL[0], 0))
                # aal['displacementCost'].append(round(othersAAL[1], 0))
                # aal['movingCost'].append(round(othersAAL[2], 0))
                # aal['workingHourLoss'].append(round(othersAAL[3], 0))

                LegacyDict['AAL'] = aal['AAL'][i]
                LegacyDict['userTypeAAL'] = aal['userTypeAAL'][i]
                LegacyDict['insurerAAL'] = aal['insurerAAL'][i]
                LegacyDict['reduction'] = aal['reduction'][i]
                LegacyDict['expectedFloodRiskReductionPerMonth'] = aal['expectedFloodRiskReductionPerMonth'][i]
                LegacyDict['expectedIndirectFloodRiskReductionPerMonth'] = aal['expectedIndirectFloodRiskReductionPerMonth'][i]
            # LegacyResults.append(LegacyDict.copy())

            # Foundation Cost

            if homeshape == "Square":
                aspect_ratio = 1.0
            elif homeshape == "Rectangle":
                aspect_ratio = 1.5
            elif homeshape == "Long":
                aspect_ratio = 2.0

            if foundationType == "Slab":
                FoundationCost, costs, materials = slab_on_fill(
                    bld_area, h+i, aspect_ratio, aspect="True", s=3, a=3, i=0.1, g=0.15, W=0.41, σ=30, t=0.1, D=0.51, h_=0.2)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'aGrading', 'vFill', 'aInsulation',
                                    'aGravel', 'vExcavation', 'aVaporBarrier', 'vSlab', 'lEdgeBeam', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio',
                                        'elevation(m)', 'aGrading', 'vFill', 'aGravel', 'vExcavation', 'aVaporBarrier', 'aInsulation', 'vSlab', 'lEdgeBeam']

            elif foundationType == "Elevated with Enclosure, Not Post, Pile, or Pier" or foundationType == "Crawlspace" or foundationType == "Basement":
                FoundationCost, costs, materials = CS1(
                    bld_area, h+i, aspect_ratio, aspect="True", i=0.1, g=0.15, W=0.41, σ=30, t=0.1, D=0.51, h_=0.2, w=0.2)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'vFill', 'aInsulation',
                                    'aGravel', 'vExcavation', 'aVaporBarrier', 'vSlab', 'lFooting', 'aGrading', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'vFill',
                                        'aInsulation', 'aGravel', 'vExcavation', 'aVaporBarrier', 'vSlab', 'lFooting', 'aGrading']

            elif foundationType == "Elevated with Enclosure, Post, Pile, or Pier":
                FoundationCost, costs, materials = CS2(
                    bld_area, h+i, aspect_ratio, aspect="True", C=0.41, P=0.25, W=0.41, t=0.1, D=0.3, h_=0.2, y=3, w=0.2)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'lPier', 'aInsulation',
                                    'aVaporBarrier', 'aGravel', 'vExcavation', 'nPad', 'vSlab', 'lFooting', 'aGrading', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'w', 'aMason', 'lPier',
                                        'aInsulation', 'aVaporBarrier', 'aGravel', 'vExcavation', 'nPad', 'vSlab', 'lFooting', 'aGrading']

            # elif foundationType=="CMU stemwalls with wood frame floor assembly on internal CMU piers":
            #     FoundationCost,costs,materials = CS3(bld_area,h+i,aspect_ratio=1.5,aspect="True",i=0.1,g=0.15,W=0.41,σ=30,t=0.1,D=0.51,h_=0.2,w=0.2)

            #     costs_df = pd.DataFrame(costs)
            #     costs_df.columns = ['Building Area','Aspect ratio','Elevation (m)','w','$_A_Mason','$_L_Pier','$_A_Vapor_Barrier','$_A_Insulation','$_A_Gravel','$_V_Excavation','$_N_Pad','$_V_Wood','$_L_Footing','$_A_Grading','$_A_Wood','Total_Cost']
            #     materials_df = pd.DataFrame(materials)
            #     materials_df.columns = ['Building Area','Aspect ratio','Elevation (m)','w','A_Mason','L_Pier','A_Vapor_Barrier','A_Insulation','A_Gravel','V_Excavation','N_Pad','V_Wood','L_Footing','A_Grading','A_Wood']

            elif foundationType == "Elevated without Enclosure, Post, Pile, or Pier":
                FoundationCost, costs, materials = CS4(bld_area, h+i, aspect_ratio, aspect="True", C=0.41, P=0.25,
                                                       W=0.41, D=0.3, h_=0.6, y=3, beam_spacing=2.44, joist_spacing=0.41, α_g=0.003319, α_j=0.002729)

                costs_df = pd.DataFrame(costs)
                costs_df.columns = ['buildingArea', 'aspectRatio', 'elevation(m)', 'lPier', 'vExcavation',
                                    'aGrading', 'aGravel', 'aInsulation', 'nPad', 'vWood', 'aWood', 'totalCost']
                materials_df = pd.DataFrame(materials)
                materials_df.columns = ['buildingArea', 'aspectRatio',
                                        'elevation(m)', 'lPier', 'vExcavation', 'aGrading', 'aGravel', 'aInsulation', 'nPad', 'vWood', 'aWood']

            costs_dict = costs_df.to_dict('list')
            materials_dict = materials_df.to_dict('list')

            for key in costResults:
                costResults[key] += costs_dict.get(key, 'nan')

            for key in materialsResults:
                materialsResults[key] += materials_dict.get(key, 'nan')

            foundationCostList.append(FoundationCost)
            foundationCostIncrease.append(FoundationCost-foundationCostList[0])
            amortizedCostPerMonth.append(round(self.calculate_AmortizedCost(
                foundationCostIncrease[-1], r, n, t), 0))

            print("LegacyDict[premiumsSavingsMonthly] = ",
                  LegacyDict["premiumsSavingsMonthly"])
            totalSavingsPerMonth.append(round(-1*amortizedCostPerMonth[-1]+aal['expectedFloodRiskReductionPerMonth']
                                        [-1]+aal['expectedIndirectFloodRiskReductionPerMonth'][-1]+LegacyDict["premiumsSavingsMonthly"], 0))

            LegacyDict['foundationCost'] = foundationCostList[i]
            LegacyDict['foundationCostIncrease'] = foundationCostIncrease[i]
            LegacyDict['amortizedCostPerMonth'] = amortizedCostPerMonth[i]
            LegacyDict['totalSavingsPerMonth'] = totalSavingsPerMonth[i]

            LegacyResults.append(LegacyDict.copy())

        FoundationCostResults = {'foundationCost': foundationCostList,
                                 'foundationCostIncrease': foundationCostIncrease,
                                 'amortizedCostPerMonth': amortizedCostPerMonth}
        maxTotalSavingsPerMonth = max(totalSavingsPerMonth)
        index = totalSavingsPerMonth.index(maxTotalSavingsPerMonth)
        optimumFFH = resultsAll[index]["firstFloorHeight"]
        print(maxTotalSavingsPerMonth, index, optimumFFH)

        return Response({'Results': resultsAll, 'maxTotalSavingsPerMonth': maxTotalSavingsPerMonth, 'optimumFFH': optimumFFH})

# Risk Rating 2.0 results


class riskrating2resultsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = riskrating2results.objects.all()
    serializer_class = riskrating2resultsSerializer

    # filter_backends = [DjangoFilterBackend,
    #                    filters.SearchFilter, filters.OrderingFilter]

    # filterset_fields = ['id', 'items']
    # search_fields = ['id', 'items']
    # ordering_fields = ['id', 'items']


class riskrating2resultsLeveeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = riskrating2resultsLevee.objects.all()
    serializer_class = riskrating2resultsLeveeSerializer

    # filter_backends = [DjangoFilterBackend,
    #                    filters.SearchFilter, filters.OrderingFilter]

    # filterset_fields = ['id', 'items']
    # search_fields = ['id', 'items']
    # ordering_fields = ['id', 'items']


# Risk Rating 2.0 inputs
class userTypeViewSet(viewsets.ModelViewSet):
    queryset = userType.objects.all()
    serializer_class = userTypeSerializer


class typeUseIDViewSet(viewsets.ModelViewSet):
    queryset = typeUseID.objects.all()
    serializer_class = typeUseIDSerializer


class homeConditionViewSet(viewsets.ModelViewSet):
    queryset = homeCondition.objects.all()
    serializer_class = homeConditionSerializer


class numOfStoriesViewSet(viewsets.ModelViewSet):
    queryset = numOfStories.objects.all()
    serializer_class = numOfStoriesSerializer


class mortgageViewSet(viewsets.ModelViewSet):
    queryset = mortgage.objects.all()
    serializer_class = mortgageSerializer


class foundationDesignIDViewSet(viewsets.ModelViewSet):
    queryset = foundationDesigns.objects.all()
    serializer_class = foundationDesignIDSerializer


class foundationTypeIDViewSet(viewsets.ModelViewSet):
    queryset = foundationTypes.objects.all()
    serializer_class = foundationTypeIDSerializer


class floodInsuranceViewSet(viewsets.ModelViewSet):
    queryset = floodInsurance.objects.all()
    serializer_class = floodInsuranceSerializer


class priorClaimsViewSet(viewsets.ModelViewSet):
    queryset = priorClaims.objects.all()
    serializer_class = priorClaimsSerializer


class federalAssistanceViewSet(viewsets.ModelViewSet):
    queryset = federalAssistance.objects.all()
    serializer_class = federalAssistanceSerializer


class investmentTypeViewSet(viewsets.ModelViewSet):
    queryset = investmentType.objects.all()
    serializer_class = investmentTypeSerializer


class homeShapeViewSet(viewsets.ModelViewSet):
    queryset = homeShape.objects.all()
    serializer_class = homeShapeSerializer


class scenarioViewSet(viewsets.ModelViewSet):
    queryset = scenario.objects.all()
    serializer_class = scenarioSerializer


class floodVentsViewSet(viewsets.ModelViewSet):
    queryset = floodVents.objects.all()
    serializer_class = floodVentsSerializer


class MandEViewSet(viewsets.ModelViewSet):
    queryset = MandE.objects.all()
    serializer_class = MandESerializer


class barrierIslandIndicatorsViewSet(viewsets.ModelViewSet):
    queryset = barrierIslandIndicators.objects.all()
    serializer_class = barrierIslandIndicatorsSerializer


class leveeIndicatorsViewSet(viewsets.ModelViewSet):
    queryset = leveeIndicators.objects.all()
    serializer_class = leveeIndicatorsSerializer


class singleFamilyHomeIndicatorViewSet(viewsets.ModelViewSet):
    queryset = singleFamilyHomeIndicator.objects.all()
    serializer_class = singleFamilyHomeIndicatorSerializer


class condoUnitOwnerIndicatorViewSet(viewsets.ModelViewSet):
    queryset = condoUnitOwnerIndicator.objects.all()
    serializer_class = condoUnitOwnerIndicatorSerializer


class primaryResidenceIndicatorViewSet(viewsets.ModelViewSet):
    queryset = primaryResidenceIndicator.objects.all()
    serializer_class = primaryResidenceIndicatorSerializer


class CRSRatingViewSet(viewsets.ModelViewSet):
    queryset = CRSRating.objects.all()
    serializer_class = CRSRatingSerializer


class buildingValueViewSet(viewsets.ModelViewSet):
    queryset = buildingValue.objects.all()
    serializer_class = buildingValueSerializer


class contentsValueViewSet(viewsets.ModelViewSet):
    queryset = contentsValue.objects.all()
    serializer_class = contentsValueSerializer


class typeOfUseViewSet(viewsets.ModelViewSet):
    queryset = typeOfUse.objects.all()
    serializer_class = typeOfUseSerializer


class floorViewSet(viewsets.ModelViewSet):
    queryset = floor.objects.all()
    serializer_class = floorSerializer


class floor1to3ViewSet(viewsets.ModelViewSet):
    queryset = floor1to3.objects.all()
    serializer_class = floor1to3Serializer


class floor1to100ViewSet(viewsets.ModelViewSet):
    queryset = floor1to100.objects.all()
    serializer_class = floor1to100Serializer


class floor1to4ViewSet(viewsets.ModelViewSet):
    queryset = floor1to4.objects.all()
    serializer_class = floor1to4Serializer

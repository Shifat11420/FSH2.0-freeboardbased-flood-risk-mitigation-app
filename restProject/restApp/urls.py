from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()


router.register(r'unitcost', views.unitcostViewSet)
router.register(r'address', views.addressViewSet)
router.register(r'addresstable', views.addresstableViewSet,
                basename='addresstable')

router.register(r'rr2-baserate', views.baserateViewSet,
                basename='rr2-baserate')
router.register(r'rr2-disttoriver', views.distToRiverViewSet,
                basename='rr2-disttoriver')
router.register(r'rr2-territory', views.territoryViewSet,
                basename='territory')
router.register(r'rr2-Nonlevee-results', views.riskrating2resultsViewSet)
router.register(r'rr2-Levee-results', views.riskrating2resultsLeveeViewSet)

router.register(r'rr2-userTypeID', views.userTypeIDViewSet)
router.register(r'rr2-typeUseID', views.typeUseIDViewSet)
router.register(r'rr2-homeCondition', views.homeConditionViewSet)
router.register(r'rr2-numOfStories', views.numOfStoriesViewSet)
router.register(r'rr2-mortgage', views.mortgageViewSet)
router.register(r'rr2-foundationDesignID', views.foundationDesignIDViewSet)
router.register(r'rr2-foundationTypeID', views.foundationTypeIDViewSet)
router.register(r'rr2-floodInsurance', views.floodInsuranceViewSet)
router.register(r'rr2-priorClaims', views.priorClaimsViewSet)
router.register(r'rr2-federalAssistance', views.federalAssistanceViewSet)
router.register(r'rr2-investmentType', views.investmentTypeViewSet)
router.register(r'rr2-homeShape', views.homeShapeViewSet)
router.register(r'rr2-floodVents', views.floodVentsViewSet)
router.register(r'rr2-MandE', views.MandEViewSet)
router.register(r'rr2-bi', views.barrierIslandIndicatorsViewSet)

router.register(r'rr2-singleFamilyHome',
                views.singleFamilyHomeIndicatorViewSet)
router.register(r'rr2-condoUnitOwner', views.condoUnitOwnerIndicatorViewSet)
router.register(r'rr2-primaryResidence',
                views.primaryResidenceIndicatorViewSet)

router.register(r'rr2-buildingValue',
                views.buildingValueViewSet)
router.register(r'rr2-contentsValue',
                views.contentsValueViewSet)
router.register(r'rr2-CRSRating',
                views.CRSRatingViewSet)
router.register(r'rr2-typeOfUse',
                views.typeOfUseViewSet)


router.register(r'rr2-scenario', views.scenarioViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CalculateNfipAPIView',
         views.CalculateNfipAPIView.as_view(), name='calcnfipapiv'),
    path('CalculateRiskAPIViewBody',
         views.CalculateRiskAPIViewBody.as_view(), name='calcriskapivbody'),
    path('RR2', views.CalculateRR2APIView.as_view(), name='rr2singlefunc')

]

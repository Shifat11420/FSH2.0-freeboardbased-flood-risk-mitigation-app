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
router.register(r'territory', views.territoryViewSet,
                basename='territory')
router.register(r'rr2-Nonlevee-results', views.riskrating2resultsViewSet)
router.register(r'rr2-Levee-results', views.riskrating2resultsLeveeViewSet)


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

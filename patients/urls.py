from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, CompanyViewSet, LocationViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'companys', CompanyViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

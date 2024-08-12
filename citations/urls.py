from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailableDaysViewSet, AvailableTimesViewSet, BookCitaViewSet

router = DefaultRouter()
router.register(r'days', AvailableDaysViewSet, basename='days')
router.register(r'available-times', AvailableTimesViewSet,
                basename='available-times')
router.register(r'book', BookCitaViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]

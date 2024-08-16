from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleBlockViewSet, AppointmentReasonViewSet, SedeViewSet, PsychologicalAppointmentViewSet

router = DefaultRouter()
router.register(r'schedule-blocks', ScheduleBlockViewSet)
router.register(r'appointment-reasons', AppointmentReasonViewSet)
router.register(r'sedes', SedeViewSet)
router.register(r'psychological-appointments', PsychologicalAppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
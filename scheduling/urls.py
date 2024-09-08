from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailableTimeSlotsView, TimeSlotViewSet, DayViewSet, DaysEmployeeViewSet, AppointmentReasonViewSet, SedeViewSet, PsychologicalAppointmentViewSet

router = DefaultRouter()
router.register(r'times', TimeSlotViewSet)
router.register(r'days', DayViewSet)
router.register(r'days-employee', DaysEmployeeViewSet)
router.register(r'appointment-reasons', AppointmentReasonViewSet)
router.register(r'sedes', SedeViewSet)
router.register(r'psychological-appointments', PsychologicalAppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('available-time-slots/', AvailableTimeSlotsView.as_view(), name='available-time-slots'),
]
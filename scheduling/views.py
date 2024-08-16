from django.db import transaction
from rest_framework import viewsets
from .models import ScheduleBlock, AppointmentReason, Sede, PsychologicalAppointment
from .serializers import ScheduleBlockSerializer, AppointmentReasonSerializer, SedeSerializer, PsychologicalAppointmentSerializer
from payments.serializers import PaymentSerializer

class ScheduleBlockViewSet(viewsets.ModelViewSet):
    queryset = ScheduleBlock.objects.all()
    serializer_class = ScheduleBlockSerializer

class AppointmentReasonViewSet(viewsets.ModelViewSet):
    queryset = AppointmentReason.objects.all()
    serializer_class = AppointmentReasonSerializer

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer

class PsychologicalAppointmentViewSet(viewsets.ModelViewSet):
    queryset = PsychologicalAppointment.objects.all()
    serializer_class = PsychologicalAppointmentSerializer
    
    @transaction.atomic
    def perform_create(self, serializer):
        appointment = serializer.save()
        
        payment_data = self.request.data.get('payment')
        payment_data['psychological_appointment'] = appointment.id
        
        payment_serializer = PaymentSerializer(data=payment_data)
        payment_serializer.is_valid(raise_exception=True)
        payment_serializer.save()
        

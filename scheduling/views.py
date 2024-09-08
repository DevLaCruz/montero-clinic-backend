from decimal import Decimal
from rest_framework.decorators import action
from django.db import transaction
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from .models import Day, DaysEmployee, TimeSlot, AppointmentReason, Sede, PsychologicalAppointment
from patients.models import Patient
from .serializers import AvailableTimeSlotsSerializer, DaySerializer, DaysEmployeeSerializer, TimeSlotSerializer, AppointmentReasonSerializer, SedeSerializer, PsychologicalAppointmentSerializer
#from payments.serializers import PaymentSerializer
import locale

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    
class DayViewSet(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    
class DaysEmployeeViewSet(viewsets.ModelViewSet):
    queryset = DaysEmployee.objects.all()
    serializer_class = DaysEmployeeSerializer
    
'''class GenerateSlotsView(APIView):
    def post(self, request):
        interval_minutes = request.data.get("interval_minutes")
        
        if not interval_minutes:
            return Response({"error": "Interval minutes is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('GenerateTimeSlots', [interval_minutes])
            
            return Response({"message": "Time slots generated successfully."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)'''

class AppointmentReasonViewSet(viewsets.ModelViewSet):
    queryset = AppointmentReason.objects.all()
    serializer_class = AppointmentReasonSerializer

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer

# CITAS PSICOLOGICAS
class PsychologicalAppointmentViewSet(viewsets.ModelViewSet):
    queryset = PsychologicalAppointment.objects.all()
    serializer_class = PsychologicalAppointmentSerializer
    
    #(Automatizar)
    @action(detail=False, methods=['post'], url_path='calculate-price')
    def calculate_price(self, request):
        patient_id = request.data.get('patient_id')
        appointment_reason_id = request.data.get('appointment_reason_id')

        if not patient_id or not appointment_reason_id:
            return Response({"error": "patient_id and appointment_reason_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient.objects.get(id=patient_id)
            appointment_reason = AppointmentReason.objects.get(id=appointment_reason_id)
        except (Patient.DoesNotExist, AppointmentReason.DoesNotExist):
            return Response({"error": "Patient or Appointment Reason not found."}, status=status.HTTP_404_NOT_FOUND)

        base_price = appointment_reason.base_price  # Esto ya es DecimalField
        percentage = Decimal(patient.company.percentage if patient.company else 0)
        price = base_price - base_price * (percentage / Decimal(100))

        return Response({"price": round(price, 2)})
    
    #Crear cita y pago
    @transaction.atomic
    def perform_create(self, serializer):
        appointment = serializer.save()
        
        payment_data = self.request.data.get('payment')
        payment_data['psychological_appointment'] = appointment.id
        
        payment_serializer = PaymentSerializer(data=payment_data)
        payment_serializer.is_valid(raise_exception=True)
        payment_serializer.save()
        
# LISTAR HORARIOS DISPONIBLES
class AvailableTimeSlotsView(APIView):
    serializer_class = AvailableTimeSlotsSerializer
    def post(self, request):
        serializer = AvailableTimeSlotsSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.validated_data.get('employee')
            date_value = serializer.validated_data.get('date')

            # Establecer la configuración regional para obtener el nombre del día en español
            locale.setlocale(locale.LC_TIME, 'es_ES')
            day_name = date_value.strftime('%A')

            # Buscar los registros de DaysEmployee que coincidan con el empleado, el día y estén habilitados
            days_employee = DaysEmployee.objects.filter(employee_id=employee, day__name=day_name.capitalize(), enabled=True)

            # Verificar si no se encontraron registros
            if not days_employee.exists():
                return Response({"error": "No se encontraron horarios disponibles para este día y empleado."}, status=status.HTTP_404_NOT_FOUND)

            # Obtener los TimeSlots asociados
            time_slots = [de.day.time_slot for de in days_employee]

            # Serializar y devolver los TimeSlots
            time_slots_serializer = TimeSlotSerializer(time_slots, many=True)
            return Response(time_slots_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
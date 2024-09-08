from decimal import Decimal
from rest_framework import serializers
from employees.serializers import EmployeeSerializer
from datetime import date
from .models import DaysEmployee, Day, TimeSlot, AppointmentReason, Sede, PsychologicalAppointment

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'
        
class DaysEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaysEmployee
        fields = '__all__'
        
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'

''''class ScheduleBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleBlock
        fields = '__all__'
        
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        date = data.get('date')
        employee = data.get('employee')

        # Verificar que el horario de inicio sea antes que el horario de finalización
        if start_time >= end_time:
            raise serializers.ValidationError('El horario de inicio debe ser antes que el horario de finalización.')

        # Verificar que no haya cruces de horarios para el mismo empleado en la misma fecha
        overlapping_blocks = ScheduleBlock.objects.filter(
            employee=employee,
            date=date
        ).exclude(id=self.instance.id if self.instance else None)

        for block in overlapping_blocks:
            if start_time < block.end_time and end_time > block.start_time:
                raise serializers.ValidationError('El horario se cruza con otro bloque de tiempo ya registrado.')

        return data'''
        
class SedeSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True,read_only=True)
    class Meta:
        model = Sede
        fields = '__all__'
        #depth = 1
        
class SimpleSedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['id', 'name', 'modality']  # Excluye 'reasons' y 'employees' si no los necesitas

class AppointmentReasonSerializer(serializers.ModelSerializer):
    sedes = SimpleSedeSerializer(many=True, read_only=True)
    class Meta:
        model = AppointmentReason
        fields = '__all__'

class PsychologicalAppointmentSerializer(serializers.ModelSerializer):
    #price = serializers.SerializerMethodField()
    class Meta:
        model = PsychologicalAppointment
        fields = '__all__'
        #depth = 1
    
    ''''def get_price(self, obj):
        base_price = obj.appointment_reason.base_price  # Esto ya es DecimalField
        percentage = Decimal(obj.patient.company.percentage if obj.patient.company else 0)
        price = base_price - base_price * (percentage / Decimal(100))
        return round(price, 2)'''

class AvailableTimeSlotsSerializer(serializers.Serializer):
    employee = serializers.IntegerField()
    date = serializers.DateField(write_only=True)

    def validate_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("La fecha debe ser posterior a la fecha actual.")
        return value
        
from rest_framework import serializers
from .models import ScheduleBlock, AppointmentReason, Sede, PsychologicalAppointment
from payments.serializers import PaymentSerializer

class ScheduleBlockSerializer(serializers.ModelSerializer):
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

        return data

class AppointmentReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentReason
        fields = '__all__'

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class PsychologicalAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalAppointment
        fields = '__all__'
        #depth = 1
        
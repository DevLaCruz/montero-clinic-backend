from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        extra_kwargs = {
            'number': {'read_only': True},
            'patient': {'write_only': True}
        }
    
    def create(self, validated_data):
        # Último número de historia médica
        last_record = MedicalRecord.objects.all().order_by('number').last()
        if not last_record:
            new_number = '000001'
        else:
            last_number = int(last_record.number)
            new_number = '{:06d}'.format(last_number + 1)
        
        # Asignar el nuevo número al validated_data
        validated_data['number'] = new_number
        
        # Crear y devolver la nueva instancia de MedicalHistory
        return super().create(validated_data)
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Patient, Company, Location

class ClientPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'is_state': {'read_only': True},
            'tutor': {'required': False, 'default': None},
            'relationship': {'required': False, 'default': None},
            'location': {'required': True},
            'company': {'required': True}
        }
        
        def validate_birth_date(self, value):
            # verificar mayor de edad
            today = timezone.now().date()
            eighteen_years_ago = today - timedelta(days=18*365.25)  # Approximate 18 years in days
            
            if value > eighteen_years_ago:
                raise serializers.ValidationError("The patient must be at least 18 years old.")
            
            return value

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'is_state': {'read_only': True},
            'user': {'read_only': True, 'default': True},
            'tutor': {'read_only': True},
        }
        #depth = 1

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
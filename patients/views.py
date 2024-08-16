from django.db import transaction
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import serializers
from rest_framework import viewsets
from .models import Patient, Company, Location
from .serializers import PatientSerializer, CompanySerializer, LocationSerializer
from medical_records.serializers import MedicalRecordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    
    @transaction.atomic
    def perform_create(self, serializer):
        # Obtenemos al patient autenticado
        patient = self.request.user.patient
        #serializer.save(tutor=patient)
        patient = serializer.save(tutor=patient)
        
        # Crear la historia médica usando el serializador
        medical_record_data = {'patient': patient.id}
        medical_history_serializer = MedicalRecordSerializer(data=medical_record_data)
        # Validar los datos antes de guardar
        medical_history_serializer.is_valid(raise_exception=True)
        
        # Guardar la historia médica después de la validación
        medical_history_serializer.save()

    def perform_update(self, serializer):
        # Al actualizar, también aseguramos de que el tutor sea el paciente autenticado
        patient = self.request.user.patient
        serializer.save(tutor=patient)
    

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
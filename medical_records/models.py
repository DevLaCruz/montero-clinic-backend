from django.db import models
from patients.models import Patient

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    number = models.CharField(max_length=6, unique=True)
    personal_history = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    physical_observations = models.TextField(blank=True, null=True)
    behavioral_observations = models.TextField(blank=True, null=True)
    personal_perception = models.TextField(blank=True, null=True)
    academic_perception = models.TextField(blank=True, null=True)
    habits = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    projections = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    sleep = models.TextField(blank=True, null=True)
    nutrition = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'Historia clinica N° {self.number} de {self.patient.first_name}'

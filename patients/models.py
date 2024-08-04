from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=255)
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

class Location(models.Model):
    code = models.CharField(max_length=6)
    department = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.department}'

class Patient(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    id_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1)
    occupation = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    id_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255)
    area = models.CharField(max_length=255)#Para estudiantes
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    #legal_guardian = models.CharField(max_length=255)
    #guardian_phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=255)#opcional
    #emergency_contact = models.CharField(max_length=255)
    emergency_phone = models.CharField(max_length=20)#opcional
    terms = models.BooleanField(default=True)
    is_state = models.BooleanField(default=True)
    benefit = models.BooleanField(default=False)#Cambie de char(100) a boolean
    id_tutor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dependents')
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

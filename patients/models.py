from django.db import models
from django.contrib.auth import get_user_model

class Company(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.IntegerField(default=0)
    change_date = models.DateField(auto_now_add=True)
    change_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}'

class Location(models.Model):
    code = models.CharField(max_length=6)
    department = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.department}-{self.province}-{self.district}'

class Patient(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)
    dni = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1)
    occupation = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255)
    area = models.CharField(max_length=255, null=True, blank=True)#opcional
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20)#Falta unico (preguntar)
    #email = models.EmailField(unique=True, null=True, blank=True)
    #legal_guardian = models.CharField(max_length=255)
    #guardian_phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=255, null=True, blank=True)
    #emergency_contact = models.CharField(max_length=255)
    emergency_phone = models.CharField(max_length=20, null=True, blank=True)
    terms = models.BooleanField(default=True)
    is_state = models.BooleanField(default=True)
    benefit = models.BooleanField(default=False)
    tutor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dependents')
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)
    marital_status = models.CharField(max_length=50, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

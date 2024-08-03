from django.contrib import admin
from .models import Patient, Company, Location

# Register your models here.
admin.site.register(Patient)
admin.site.register(Company)
admin.site.register(Location)

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from patients.models import Location

class Employee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    sex = models.CharField(max_length=1)
    profession = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=9)
    email = models.EmailField(max_length=50)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        import datetime
        today = datetime.date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

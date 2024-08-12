from django.contrib.auth.models import User
from django.db import models


class Holiday(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class AvailableTimeSlot(models.Model):
    # e.g., "Monday", "Tuesday", etc.
    day_of_week = models.CharField(max_length=9)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"


class Citation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    # Aquí '1' es un ejemplo de ID de un time_slot válido
    time_slot = models.ForeignKey(
        AvailableTimeSlot, on_delete=models.CASCADE, default=1)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('date', 'time_slot')

    def __str__(self):
        return f"{self.date} {self.time_slot} - {self.user.username}"

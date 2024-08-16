from django.db import models
from patients.models import Patient
from employees.models import Employee

class ScheduleBlock(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()  # Schedule date
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)

    def __str__(self):
        return f"Horario Bloque {self.id} - {self.date} - {self.employee}"

# Motivo de la cita
class AppointmentReason(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.TextField()
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.reason

class Sede(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    status = models.BooleanField(default=True)
    change_date = models.DateField(auto_now=True)
    change_time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.name

class PsychologicalAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    schedule_block = models.ForeignKey(ScheduleBlock, on_delete=models.CASCADE)
    appointment_reason = models.ForeignKey(AppointmentReason, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, default='Programada')
    modality = models.CharField(max_length=1, default='P', choices=[('P', 'Presencial'), ('V', 'Virtual')])

    def __str__(self):
        return f"Appointment {self.id} - {self.patient} - {self.status}"
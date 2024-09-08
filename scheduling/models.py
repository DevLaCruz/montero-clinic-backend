from django.db import models
from patients.models import Patient
from employees.models import Employee

class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    enabled = models.BooleanField(default=True)
    duration = models.IntegerField()
    change_date = models.DateField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
    
class Day(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    enabled = models.BooleanField(default=True)
    change_date = models.DateField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DaysEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    change_date = models.DateField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Personal {self.employee.last_name} - Day {self.day} - {self.day.time_slot}"

# Motivo de la cita (Servicios)
class AppointmentReason(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0)
    modality = models.CharField(max_length=1, default='A', choices=[('P', 'Presencial'), ('V', 'Virtual'),('A', 'Ambos')])
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
    modality = models.CharField(max_length=1, default='A', choices=[('P', 'Presencial'), ('V', 'Virtual'),('A', 'Ambos')])
    employees = models.ManyToManyField(Employee, related_name='sedes')
    reasons = models.ManyToManyField(AppointmentReason, related_name='sedes')

    def __str__(self):
        return self.name

class PsychologicalAppointment(models.Model):
    ## Colocar el start y en final
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    days_employee = models.ForeignKey(DaysEmployee, on_delete=models.CASCADE)
    appointment_reason = models.ForeignKey(AppointmentReason, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    date = models.DateField()
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    # P = Pendiente de pago, P = Por validar, A = Agendada, F = Atendida, R = Reprogramada
    status = models.CharField(max_length=15, default='Pendiente de pago')
    modality = models.CharField(max_length=1, default='P', choices=[('P', 'Presencial'), ('V', 'Virtual')])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"Appointment {self.id} - {self.patient} - {self.status}"
from django.db import models
from scheduling.models import PsychologicalAppointment

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    psychological_appointment = models.OneToOneField(PsychologicalAppointment, on_delete=models.CASCADE)# Corresponde Cita psicologica
    payment_date = models.DateField(auto_now_add=True)  # Corresponde a fechaPago
    amount = models.DecimalField(max_digits=7, decimal_places=2)  # Corresponde a importe
    payment_image = models.ImageField(upload_to='payment_images/', null=True, blank=True)  # Corresponde a voucher
    status = models.CharField(max_length=1, choices=[('S', 'Verified'), ('N', 'Not Verified')], default='N')  # Corresponde a estado
    change_date = models.DateField(auto_now=True)  # fechaCambio
    change_time = models.TimeField(auto_now=True)  # tiempo

    def __str__(self):
        return f"Payment {self.id} for Appointment {self.psychological_appointment.id} - Status: {self.get_status_display()}"


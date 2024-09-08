from django.contrib import admin
from .models import Day, DaysEmployee, TimeSlot, AppointmentReason, Sede, PsychologicalAppointment

admin.site.register(TimeSlot)
admin.site.register(Day)
admin.site.register(DaysEmployee)
admin.site.register(AppointmentReason)
admin.site.register(Sede)
admin.site.register(PsychologicalAppointment)
from django.contrib import admin
from .models import ScheduleBlock, AppointmentReason, Sede, PsychologicalAppointment

admin.site.register(ScheduleBlock)
admin.site.register(AppointmentReason)
admin.site.register(Sede)
admin.site.register(PsychologicalAppointment)
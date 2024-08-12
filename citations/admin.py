
# citations/admin.py

from django.contrib import admin
from .models import Citation, AvailableTimeSlot, Holiday


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date',)
    ordering = ('date',)


@admin.register(AvailableTimeSlot)
class AvailableTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time')
    ordering = ('day_of_week', 'start_time')


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time_slot')
    ordering = ('date', 'time_slot')
    readonly_fields = ('user', 'date', 'time_slot')

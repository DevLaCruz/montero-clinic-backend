# admin.py
from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'phone_number', 'status')

    def status(self, obj):
        return 'Pendiente por activar' if not obj.is_active else 'Activo'

    status.short_description = 'Estado'


admin.site.register(Account, AccountAdmin)

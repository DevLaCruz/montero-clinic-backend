from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser', 'is_worker', 'last_login', 'date_joined')

    # Define los fieldsets para la vista de edición de usuarios (sin 'last_login' ni 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('is_worker',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Define los add_fieldsets para la vista de creación de usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_worker', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_staff', 'is_active', 'is_worker')

# Registra el modelo User con la clase UserAdmin personalizada
admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Datos del sistema", {"fields": ("rol",)}),)
    list_display = ("username", "first_name", "last_name", "email", "rol", "is_active")
    list_filter = ("rol", "is_active", "is_staff")

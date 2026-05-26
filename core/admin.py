from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil Lírion', {'fields': ('foto', 'bio')}),
    )
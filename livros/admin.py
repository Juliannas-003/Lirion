from django.contrib import admin
from .models import Livro, StatusLeitura


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'ano']
    search_fields = ['titulo', 'autor']


@admin.register(StatusLeitura)
class StatusLeituraAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'livro', 'status', 'data_atualizacao']
    list_filter = ['status']
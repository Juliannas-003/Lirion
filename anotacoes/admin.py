from django.contrib import admin
from .models import Anotacao


@admin.register(Anotacao)
class AnotacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'livro', 'data_criacao']
    search_fields = ['texto']
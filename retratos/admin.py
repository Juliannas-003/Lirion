from django.contrib import admin
from .models import Retrato, Recomendacao


@admin.register(Retrato)
class RetratoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'livro', 'data_geracao']


@admin.register(Recomendacao)
class RecomendacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'livro_sugerido', 'data_geracao']
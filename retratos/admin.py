from django.contrib import admin
from .models import Retrato, PlanoLeitura, PlanoGenero, PlanoLivroSugerido

admin.site.register(Retrato)
admin.site.register(PlanoLeitura)
admin.site.register(PlanoGenero)
admin.site.register(PlanoLivroSugerido)
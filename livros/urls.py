from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('buscar/', views.buscar, name='buscar'),
    path('adicionar/', views.adicionar, name='adicionar'),
    path('estante/', views.estante, name='estante'),
    path('remover/<int:status_id>/', views.remover, name='remover'),
    path('mudar-status/<int:status_id>/', views.mudar_status, name='mudar_status'),
]
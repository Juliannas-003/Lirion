from django.urls import path
from . import views

app_name = 'retratos'

urlpatterns = [
    path('retrato/<int:livro_id>/', views.ver_retrato, name='ver_retrato'),
    path('plano/', views.criar_plano, name='criar_plano'),
    path('plano/<int:plano_id>/', views.ver_plano, name='ver_plano'),
    path('historico/', views.historico_planos, name='historico'),
]

# urls py de retratos 
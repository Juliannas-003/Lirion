from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/cadastro/', views.cadastro, name='cadastro'),
]
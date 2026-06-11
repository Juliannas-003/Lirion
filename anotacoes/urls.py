from django.urls import path
from . import views

app_name = 'anotacoes'

urlpatterns = [
    path('livro/<int:livro_id>/', views.pagina_livro, name='pagina_livro'),
    path('livro/<int:livro_id>/salvar/', views.salvar_anotacao, name='salvar'),
    path('<int:pk>/editar/', views.editar_anotacao, name='editar'),
    path('<int:pk>/deletar/', views.deletar_anotacao, name='deletar'),
    path('livro/<int:livro_id>/concluir/', views.concluir_leitura, name='concluir'),
]
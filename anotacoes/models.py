from django.db import models
from django.conf import settings
from livros.models import Livro


class Anotacao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='anotacoes'
    )
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='anotacoes'
    )
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Anotação de {self.usuario} em {self.livro.titulo}"
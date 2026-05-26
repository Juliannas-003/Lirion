from django.db import models
from django.conf import settings
from livros.models import Livro


class Retrato(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='retratos'
    )
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='retratos'
    )
    conteudo = models.TextField()
    data_geracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'livro']
        ordering = ['-data_geracao']

    def __str__(self):
        return f"Retrato de {self.usuario} — {self.livro.titulo}"


class Recomendacao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recomendacoes'
    )
    livro_sugerido = models.CharField(max_length=300)
    autor_sugerido = models.CharField(max_length=200, blank=True)
    justificativa = models.TextField()
    humor_informado = models.CharField(max_length=200, blank=True)
    genero_informado = models.CharField(max_length=200, blank=True)
    data_geracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_geracao']

    def __str__(self):
        return f"Recomendação para {self.usuario}: {self.livro_sugerido}"
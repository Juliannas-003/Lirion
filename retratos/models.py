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


class PlanoLeitura(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planos'
    )
    # Inputs do usuário
    paginas_por_hora = models.FloatField()
    horas_por_dia = models.FloatField()
    quantidade_livros = models.IntegerField()
    texto_livre = models.TextField(blank=True)

    # Resultado gerado
    conteudo_ia = models.TextField(blank=True)
    duracao_estimada_dias = models.IntegerField(null=True, blank=True)

    data_geracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_geracao']

    def __str__(self):
        return f"Plano de {self.usuario.username} — {self.data_geracao:%d/%m/%Y}"


class PlanoGenero(models.Model):
    plano = models.ForeignKey(
        PlanoLeitura,
        on_delete=models.CASCADE,
        related_name='generos'
    )
    genero = models.CharField(max_length=100)
    subgenero = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.genero} — {self.plano}"


class PlanoLivroSugerido(models.Model):
    plano = models.ForeignKey(
        PlanoLeitura,
        on_delete=models.CASCADE,
        related_name='livros_sugeridos'
    )
    ordem = models.IntegerField()
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200, blank=True)
    paginas_estimadas = models.IntegerField(null=True, blank=True)
    semana_sugerida = models.IntegerField(null=True, blank=True)
    justificativa = models.TextField(blank=True)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.ordem}. {self.titulo}"
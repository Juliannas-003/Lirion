from django.db import models
from django.conf import settings


class Livro(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    capa_url = models.URLField(blank=True)
    sinopse = models.TextField(blank=True)
    ano = models.IntegerField(null=True, blank=True)
    ol_key = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} — {self.autor}"


class StatusLeitura(models.Model):
    STATUS_CHOICES = [
        ('lido', 'Lido'),
        ('lendo', 'Lendo'),
        ('quero_ler', 'Quero Ler'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='status_leituras'
    )
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='quero_ler'
    )
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['usuario', 'livro']

    def __str__(self):
        return f"{self.usuario} — {self.livro.titulo} ({self.status})"
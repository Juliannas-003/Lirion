from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    foto = models.ImageField(
        upload_to='perfis/',
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True,
        max_length=500
    )

    def __str__(self):
        return self.username


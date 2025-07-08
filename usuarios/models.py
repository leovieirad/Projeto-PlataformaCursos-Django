from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Usuario(AbstractUser):
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
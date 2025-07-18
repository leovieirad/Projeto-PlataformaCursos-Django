from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    titulo = models.CharField(max_length=60, blank=True)
    bio = models.TextField(blank=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    tiktok_user = models.CharField(max_length=50, blank=True)
    x_user = models.CharField("Usuário do X", max_length=50, blank=True)
    youtube_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Usuario(AbstractUser):
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    pontos = models.IntegerField(default=0)
    ultima_insignia = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.ultima_insignia:
            self.ultima_insignia = self.insignea
        super().save(*args, **kwargs)

    @property
    def insignea(self):
        if self.pontos >= 140:
            return "🏆 Mestre"
        elif self.pontos >= 100:
            return "🥇 Avançado"
        elif self.pontos >= 80:
            return "🥈 Intermediário"
        elif self.pontos >= 50:
            return "🥉 Iniciante"
        return "🔰 Novato"


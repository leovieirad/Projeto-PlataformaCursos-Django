from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='cursos/imagens/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Aula(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=100)
    video_url = models.URLField(blank=True)
    conteudo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.curso.titulo})"
    
class Matricula(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"

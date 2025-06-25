from django.contrib import admin
from .models import Curso, Aula

class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [AulaInline]

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso')

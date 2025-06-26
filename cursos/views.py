from django.shortcuts import render
from .models import Curso
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

def detalhe_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    aulas = curso.aulas.all()
    return render(request, 'cursos/detalhe_curso.html', {'curso': curso, 'aulas': aulas})

@login_required
def matricular_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    Matricula.objects.get_or_create(usuario=request.user, curso=curso)
    return HttpResponseRedirect(reverse('detalhe_curso', args=[slug]))
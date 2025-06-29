from .models import Curso, Aula, AulaAssistida, Matricula
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse



def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

def detalhe_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    aulas = Aula.objects.filter(curso=curso)
    
    esta_matriculado = False
    aulas_assistidas_ids = []
    progresso_percentual = 0
    aulas_assistidas = 0
    total_aulas = aulas.count()

    if request.user.is_authenticated:
        esta_matriculado = curso.matriculas.filter(usuario=request.user).exists()

        # IDs das aulas assistidas (para o template saber quais já foram marcadas)
        aulas_assistidas_ids = AulaAssistida.objects.filter(
            usuario=request.user,
            aula__in=aulas
        ).values_list('aula_id', flat=True)

        # Contagem de aulas assistidas para progresso
        aulas_assistidas = AulaAssistida.objects.filter(
            usuario=request.user,
            aula__in=aulas
        ).count()

        if total_aulas > 0:
            progresso_percentual = int((aulas_assistidas / total_aulas) * 100)

    return render(request, 'cursos/detalhe_curso.html', {
        'curso': curso,
        'aulas': aulas,
        'esta_matriculado': esta_matriculado,
        'aulas_assistidas_ids': aulas_assistidas_ids,
        'aulas_assistidas': aulas_assistidas,
        'total_aulas': total_aulas,
        'progresso_percentual': progresso_percentual,
    })

@login_required
def matricular_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    Matricula.objects.get_or_create(usuario=request.user, curso=curso)
    return HttpResponseRedirect(reverse('detalhe_curso', args=[slug]))


@login_required
def marcar_aula_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    AulaAssistida.objects.get_or_create(usuario=request.user, aula=aula)

    return redirect('detalhe_curso', slug=aula.curso.slug)

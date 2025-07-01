from .models import Curso, Aula, AulaAssistida, Matricula
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ComentarioForm



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
    comentarios = curso.comentarios.all().order_by('-criado_em')
    form_comentario = ComentarioForm()

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
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    })


@login_required
def matricular_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    Matricula.objects.get_or_create(usuario=request.user, curso=curso)
    return HttpResponseRedirect(reverse('detalhe_curso', args=[slug]))

@login_required
def desmatricular_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    Matricula.objects.filter(usuario=request.user, curso=curso).delete()
    return redirect('detalhe_curso', slug=curso.slug)

@login_required
def marcar_aula_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    AulaAssistida.objects.get_or_create(usuario=request.user, aula=aula)

    return redirect('detalhe_curso', slug=aula.curso.slug)

@login_required
def desmarcar_aula_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    AulaAssistida.objects.filter(usuario=request.user, aula=aula).delete()
    return redirect('detalhe_curso', slug=aula.curso.slug)

@login_required
def comentar_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.curso = curso
            comentario.save()
    return redirect('detalhe_curso', slug=slug)

@login_required
def ver_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    curso = aula.curso
    aulas = Aula.objects.filter(curso=curso).order_by('id')
    
    # IDs de aulas assistidas
    assistidas = AulaAssistida.objects.filter(usuario=request.user, aula__in=aulas).values_list('aula_id', flat=True)
    
    # Encontrar próxima aula
    proxima = aulas.filter(id__gt=aula_id).first()
    
    return render(request, 'cursos/ver_aula.html', {
        'curso': curso,
        'aulas': aulas,
        'aula_atual': aula,
        'assistidas': assistidas,
        'proxima_aula': proxima
    })
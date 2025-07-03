from .models import Curso, Aula, AulaAssistida, Matricula
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import ComentarioForm




def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

def detalhe_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    aulas = Aula.objects.filter(curso=curso).order_by('id')
    esta_matriculado = False
    aula_atual = None
    aulas_assistidas_ids = []

    if request.user.is_authenticated:
        esta_matriculado = Matricula.objects.filter(usuario=request.user, curso=curso).exists()

        aula_id = request.GET.get('aula')
        if aula_id:
            aula_atual = get_object_or_404(Aula, id=aula_id, curso=curso)
        elif aulas.exists():
            aula_atual = aulas.first()

        aulas_assistidas_ids = list(
            AulaAssistida.objects.filter(usuario=request.user, aula__curso=curso).values_list('aula_id', flat=True)
        )
    else:
        aula_atual = aulas.first() if aulas.exists() else None

    progresso_percentual = (
        int((len(aulas_assistidas_ids) / aulas.count()) * 100) if aulas.exists() else 0
    )

    comentarios = curso.comentarios.all().order_by('-criado_em')
    form_comentario = ComentarioForm()

    contexto = {
        'curso': curso,
        'aulas': aulas,
        'aula_atual': aula_atual,
        'esta_matriculado': esta_matriculado,
        'aulas_assistidas_ids': aulas_assistidas_ids,  # variável correta
        'progresso_percentual': progresso_percentual,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    }

    return render(request, 'cursos/detalhe_curso.html', contexto)

   
@login_required
def matricular_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    Matricula.objects.get_or_create(usuario=request.user, curso=curso)
    return HttpResponseRedirect(reverse('detalhe_curso', args=[slug]))

@login_required
def desmatricular_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    Matricula.objects.filter(usuario=request.user, curso=curso).delete()
    return redirect('lista_cursos')



@login_required
def marcar_aula_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    AulaAssistida.objects.get_or_create(usuario=request.user, aula=aula)
    return redirect(f"{reverse('detalhe_curso', args=[aula.curso.slug])}?aula={aula.id}")

@login_required
def desmarcar_aula_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    AulaAssistida.objects.filter(usuario=request.user, aula=aula).delete()
    return redirect(f"{reverse('detalhe_curso', args=[aula.curso.slug])}?aula={aula.id}")


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



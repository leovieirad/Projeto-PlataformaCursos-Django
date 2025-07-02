from .models import Curso, Aula, AulaAssistida, Matricula
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import ComentarioForm
from django.views.decorators.csrf import csrf_exempt
import json


def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

def detalhe_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    aulas = Aula.objects.filter(curso=curso).order_by('id')
    esta_matriculado = False
    aula_atual = None

    if request.user.is_authenticated:
        esta_matriculado = Matricula.objects.filter(usuario=request.user, curso=curso).exists()

        # Aula atual baseada no parâmetro GET
        aula_id = request.GET.get('aula')
        if aula_id:
            aula_atual = get_object_or_404(Aula, id=aula_id, curso=curso)
        elif aulas.exists():
            aula_atual = aulas.first()
    else:
        aula_atual = aulas.first() if aulas.exists() else None

    # Aulas assistidas
    aulas_assistidas = []
    if request.user.is_authenticated:
        aulas_assistidas = AulaAssistida.objects.filter(usuario=request.user, aula__curso=curso).values_list('aula_id', flat=True)

    comentarios = curso.comentarios.all().order_by('-criado_em')
    form_comentario = ComentarioForm()

    contexto = {
        'curso': curso,
        'aulas': aulas,
        'aula_atual': aula_atual,
        'esta_matriculado': esta_matriculado,
        'assistidas': aulas_assistidas,
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


@csrf_exempt
@login_required
def toggle_assistida(request, aula_id):
    if request.method == 'POST':
        aula = get_object_or_404(Aula, id=aula_id)
        data = json.loads(request.body)
        assistida = data.get('assistida', False)

        if assistida:
            AulaAssistida.objects.get_or_create(usuario=request.user, aula=aula)
        else:
            AulaAssistida.objects.filter(usuario=request.user, aula=aula).delete()

        curso = aula.curso
        total = curso.aulas.count()
        assistidas = AulaAssistida.objects.filter(usuario=request.user, aula__curso=curso).count()
        progresso = int((assistidas / total) * 100) if total > 0 else 0

        return JsonResponse({'progresso': progresso})
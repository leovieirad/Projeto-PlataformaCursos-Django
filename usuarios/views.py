from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from cursos.models import Matricula, AulaAssistida, Aula
from django.contrib.auth.decorators import login_required


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = '' 


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})


def logar_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lista_cursos')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def deslogar_usuario(request):
    logout(request)
    return redirect('lista_cursos')



@login_required
def meus_cursos(request):
    matriculas = Matricula.objects.filter(usuario=request.user)
    progresso = {}

    for m in matriculas:
        total = m.curso.aulas.count()
        assistidas = AulaAssistida.objects.filter(aula__curso=m.curso, usuario=request.user).count()
        progresso[m.curso.id] = {
            'total': total,
            'assistidas': assistidas,
            'percentual': int((assistidas / total) * 100) if total else 0
        }

    return render(request, 'usuarios/meus_cursos.html', {
        'matriculas': matriculas,
        'progresso': progresso
    })


@login_required
def perfil_usuario(request):
    usuario = request.user
    matriculas = Matricula.objects.filter(usuario=usuario)
    progresso = {}

    for m in matriculas:
        total = m.curso.aulas.count()
        assistidas = m.curso.aulas_assistidas_por_usuario(usuario).count()  # <-- aqui estava o erro
        progresso[m.curso.id] = {
            'total': total,
            'assistidas': assistidas,
            'percentual': int((assistidas / total) * 100) if total else 0
        }

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'matriculas': matriculas,
        'progresso': progresso
    })

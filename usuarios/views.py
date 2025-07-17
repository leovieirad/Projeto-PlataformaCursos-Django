from .forms import UsuarioForm, PerfilForm
from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from cursos.models import Matricula, AulaAssistida, Aula
from django.contrib.auth.decorators import login_required
from .models import Perfil, Usuario

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
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
    perfil, _ = Perfil.objects.get_or_create(user=usuario)
    matriculas = Matricula.objects.filter(usuario=usuario)

    for m in matriculas:
        aulas = Aula.objects.filter(curso=m.curso)
        total = aulas.count()
        assistidas = AulaAssistida.objects.filter(usuario=usuario, aula__in=aulas).count()
        percentual = int((assistidas / total) * 100) if total else 0
        m.progresso = {'total': total, 'assistidas': assistidas, 'percentual': percentual}

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=usuario)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)

        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Dados atualizados com sucesso.")
            return redirect('perfil')
    else:
        usuario_form = UsuarioForm(instance=usuario)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'matriculas': matriculas,
        'form': usuario_form,
        'perfil_form': perfil_form,
    })

def ranking_usuarios(request):
    usuarios = User.objects.order_by('-pontos')
    return render(request, 'usuarios/ranking.html', {'usuarios': usuarios})

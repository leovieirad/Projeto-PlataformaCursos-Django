from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from cursos.models import Matricula
from django.contrib.auth.decorators import login_required

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
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
    return render(request, 'usuarios/meus_cursos.html', {'matriculas': matriculas})


from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('login/', views.logar_usuario, name='login'),
    path('logout/', views.deslogar_usuario, name='logout'),
    path('meus-cursos/', views.meus_cursos, name='meus_cursos'),

]
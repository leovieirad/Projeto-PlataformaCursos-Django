from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<slug:slug>/', views.detalhe_curso, name='detalhe_curso'),
    path('<slug:slug>/matricular/', views.matricular_curso, name='matricular_curso'),
    path('aula/<int:aula_id>/assistir/', views.marcar_aula_assistida, name='marcar_aula_assistida'),
]

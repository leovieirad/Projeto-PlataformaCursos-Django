from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<slug:slug>/', views.detalhe_curso, name='detalhe_curso'),
    path('<slug:slug>/matricular/', views.matricular_curso, name='matricular_curso'),
    path('aula/<int:aula_id>/marcar/', views.marcar_aula, name='marcar_aula'),
    path('aula/<int:aula_id>/desmarcar/', views.desmarcar_aula_assistida, name='desmarcar_aula'),
    path('<slug:slug>/desmatricular/', views.desmatricular_curso, name='desmatricular_curso'),
    path('<slug:slug>/comentar/', views.comentar_curso, name='comentar_curso'),

]

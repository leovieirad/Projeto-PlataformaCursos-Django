from django import forms
from django.contrib.auth import get_user_model
from .models import Perfil

Usuario = get_user_model()

class UsuarioForm(forms.ModelForm):
    foto = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name']

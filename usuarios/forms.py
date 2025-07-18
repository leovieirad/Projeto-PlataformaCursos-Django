from django import forms
from django.contrib.auth import get_user_model
from .models import Perfil


Usuario = get_user_model()

class UsuarioForm(forms.ModelForm):
    foto = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name']


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'foto', 'titulo', 'bio',
            'facebook_url', 'instagram_url', 'linkedin_url',
            'tiktok_user', 'x_user', 'youtube_url'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

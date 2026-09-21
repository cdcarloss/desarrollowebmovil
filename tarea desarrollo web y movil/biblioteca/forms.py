from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Libro


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=150)
    password = forms.CharField(label="Contrasena", widget=forms.PasswordInput)


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            "titulo",
            "isbn",
            "anio_publicacion",
            "ejemplares_disponibles",
            "autor",
            "categorias",
        ]
        widgets = {
            "categorias": forms.CheckboxSelectMultiple,
        }

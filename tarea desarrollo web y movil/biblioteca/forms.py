from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import Comentario, Empleado, JuegoMesa, Libro, LibroEbook, LibroFisico, Perfil, Prestamo, Socio


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario", max_length=150, widget=forms.TextInput(attrs={"minlength": 3})
    )
    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(attrs={"minlength": 8})
    )


class LibroFisicoForm(forms.ModelForm):
    class Meta:
        model = LibroFisico
        fields = ["titulo", "isbn", "anio_publicacion", "stock", "autor", "ubicacion", "imagen"]
        widgets = {
            "isbn": forms.TextInput(attrs={"minlength": 10}),
            "ubicacion": forms.TextInput(attrs={"minlength": 2, "placeholder": "Ej: Estante A-12"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Django fija min=0 al crear estos campos numericos; el rango real se declara aqui.
        self.fields["anio_publicacion"].widget.attrs.update({"min": 1450, "max": timezone.now().year})
        self.fields["autor"].empty_label = "Selecciona un autor"


class LibroEbookForm(forms.ModelForm):
    class Meta:
        model = LibroEbook
        fields = ["titulo", "isbn", "anio_publicacion", "stock", "autor", "formato_archivo", "tamano_mb", "imagen"]
        widgets = {"isbn": forms.TextInput(attrs={"minlength": 10})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["anio_publicacion"].widget.attrs.update({"min": 1450, "max": timezone.now().year})
        self.fields["tamano_mb"].widget.attrs["min"] = 1
        self.fields["autor"].empty_label = "Selecciona un autor"


class JuegoMesaForm(forms.ModelForm):
    class Meta:
        model = JuegoMesa
        fields = ["nombre", "marca", "categoria", "jugadores_min", "jugadores_max", "edad_minima", "stock", "imagen"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in ("jugadores_min", "jugadores_max"):
            self.fields[campo].widget.attrs["min"] = 1
        self.fields["edad_minima"].widget.attrs["min"] = 0


class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ["nombre", "correo", "telefono"]
        widgets = {
            "nombre": forms.TextInput(attrs={"minlength": 3}),
            "telefono": forms.TextInput(attrs={"data-formato": "telefono"}),
        }


class PrestamoForm(forms.ModelForm):
    """Formulario para registrar un préstamo en el mesón (siempre con un
    bibliotecario a cargo). El pedido que el propio socio hace desde su
    lista de préstamos no usa este formulario: lo arma la vista de
    checkout directamente (ver views.checkout)."""

    class Meta:
        model = Prestamo
        fields = ["libro", "juego", "socio", "empleado"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["libro"].queryset = Libro.objects.con_stock().select_related("autor")
        self.fields["libro"].required = False
        self.fields["libro"].empty_label = "— Ningún libro —"
        self.fields["juego"].queryset = JuegoMesa.objects.filter(stock__gt=0)
        self.fields["juego"].required = False
        self.fields["juego"].empty_label = "— Ningún juego —"
        self.fields["socio"].empty_label = "Selecciona un socio"
        self.fields["empleado"].queryset = Empleado.objects.filter(activo=True)
        self.fields["empleado"].empty_label = "Selecciona un empleado"
        # El modelo permite empleado vacío (lo usa el checkout del portal),
        # pero el registro hecho en el mesón siempre debe indicar quién atendió.
        self.fields["empleado"].required = True


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["foto", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3, "maxlength": 280, "placeholder": "Cuéntanos algo sobre ti"}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(
                attrs={"rows": 3, "minlength": 5, "placeholder": "¿Qué te pareció este libro?"}
            ),
        }

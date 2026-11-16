from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol")
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "rol": "Rol",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email", "rol", "is_active")
        labels = {"first_name": "Nombre", "last_name": "Apellido", "email": "Correo", "rol": "Rol", "is_active": "Usuario activo"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, "attrs"):
                field.widget.attrs["class"] = "form-control"

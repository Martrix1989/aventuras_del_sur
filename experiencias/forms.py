from django import forms
from .models import Categoria, Experiencia


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nombre", "descripcion", "activo")
        labels = {"nombre": "Nombre", "descripcion": "Descripción", "activo": "Categoría activa"}
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ExperienciaForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        label="Fecha y hora",
    )

    class Meta:
        model = Experiencia
        fields = ("titulo", "descripcion", "precio", "cupo_maximo", "fecha_hora", "categoria", "estado")
        labels = {"titulo": "Título", "descripcion": "Descripción", "precio": "Precio (CLP)", "cupo_maximo": "Cupo máximo", "categoria": "Categoría", "estado": "Experiencia activa"}
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].queryset = Categoria.objects.filter(activo=True)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

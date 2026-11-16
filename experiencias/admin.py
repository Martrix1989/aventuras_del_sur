from django.contrib import admin
from .models import Categoria, Experiencia, Inscripcion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "creador", "fecha_hora", "cupo_maximo", "estado")
    list_filter = ("estado", "categoria")
    search_fields = ("titulo", "descripcion")

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "experiencia", "fecha_inscripcion", "estado_pago")
    list_filter = ("estado_pago",)

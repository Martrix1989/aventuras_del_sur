from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from cuentas.decorators import roles_permitidos
from .models import Categoria, Experiencia, Inscripcion
from .forms import CategoriaForm, ExperienciaForm


def lista_experiencias(request):
    consulta = Experiencia.objects.select_related("categoria", "creador")
    if not request.user.is_authenticated:
        # El catálogo activo es público; reservar exige iniciar sesión como turista.
        experiencias = consulta.filter(estado=True, fecha_hora__gt=timezone.now())
    elif request.user.rol == "admin":
        experiencias = consulta.all()
    elif request.user.rol == "guia":
        experiencias = consulta.filter(creador=request.user)
    else:
        experiencias = consulta.filter(estado=True, fecha_hora__gt=timezone.now())
    return render(request, "experiencias/lista.html", {"experiencias": experiencias})


@roles_permitidos("admin", "guia")
def crear_experiencia(request):
    form = ExperienciaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        experiencia = form.save(commit=False)
        experiencia.creador = request.user
        experiencia.save()
        messages.success(request, "Experiencia creada correctamente.")
        return redirect("experiencias:lista")
    return render(request, "shared/form.html", {"form": form, "titulo": "Nueva experiencia", "volver": "experiencias:lista"})


@roles_permitidos("admin", "guia")
def editar_experiencia(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk)
    if request.user.rol == "guia" and experiencia.creador_id != request.user.id:
        raise PermissionDenied("Solo puedes editar experiencias creadas por ti.")
    form = ExperienciaForm(request.POST or None, instance=experiencia)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experiencia actualizada correctamente.")
        return redirect("experiencias:lista")
    return render(request, "shared/form.html", {"form": form, "titulo": "Editar experiencia", "volver": "experiencias:lista"})


@roles_permitidos("admin")
@require_POST
def eliminar_experiencia(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk)
    experiencia.delete()
    messages.success(request, "Experiencia eliminada.")
    return redirect("experiencias:lista")


@roles_permitidos("admin")
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "experiencias/categorias.html", {"categorias": categorias})


@roles_permitidos("admin")
def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría creada correctamente.")
        return redirect("experiencias:categorias")
    return render(request, "shared/form.html", {"form": form, "titulo": "Nueva categoría", "volver": "experiencias:categorias"})


@roles_permitidos("admin")
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría actualizada correctamente.")
        return redirect("experiencias:categorias")
    return render(request, "shared/form.html", {"form": form, "titulo": "Editar categoría", "volver": "experiencias:categorias"})


@roles_permitidos("admin")
@require_POST
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    try:
        categoria.delete()
        messages.success(request, "Categoría eliminada.")
    except Exception:
        messages.error(request, "No se puede eliminar: hay experiencias asociadas a esta categoría.")
    return redirect("experiencias:categorias")


@roles_permitidos("turista")
@require_POST
def reservar_experiencia(request, pk):
    with transaction.atomic():
        experiencia = get_object_or_404(
            Experiencia.objects.select_for_update(),
            pk=pk,
            estado=True,
            fecha_hora__gt=timezone.now(),
        )
        # Toda inscripción ocupa un cupo, aunque el pago esté pendiente.
        reservas_existentes = Inscripcion.objects.filter(experiencia=experiencia).count()
        if reservas_existentes >= experiencia.cupo_maximo:
            messages.error(request, "No quedan cupos disponibles para esta experiencia.")
            return redirect("experiencias:lista")
        try:
            Inscripcion.objects.create(usuario=request.user, experiencia=experiencia)
            messages.success(request, "Tu inscripción quedó registrada con pago pendiente.")
        except IntegrityError:
            messages.warning(request, "Ya tienes una reserva para esta experiencia.")
    return redirect("experiencias:mis_reservas")


@login_required
def mis_reservas(request):
    if request.user.rol == "admin":
        reservas = Inscripcion.objects.select_related("usuario", "experiencia").all()
        titulo = "Todas las reservas"
    elif request.user.rol == "turista":
        reservas = Inscripcion.objects.select_related("usuario", "experiencia").filter(usuario=request.user)
        titulo = "Mis reservas"
    elif request.user.rol == "guia":
        reservas = Inscripcion.objects.select_related("usuario", "experiencia").filter(experiencia__creador=request.user)
        titulo = "Reservas de mis experiencias"
    else:
        raise PermissionDenied
    return render(request, "experiencias/reservas.html", {"reservas": reservas, "titulo": titulo})


@roles_permitidos("admin")
@require_POST
def cambiar_estado_reserva(request, pk):
    reserva = get_object_or_404(Inscripcion, pk=pk)
    nuevo_estado = request.POST.get("estado_pago")
    if nuevo_estado in Inscripcion.EstadosPago.values:
        reserva.estado_pago = nuevo_estado
        reserva.save(update_fields=["estado_pago"])
        messages.success(request, "Estado de pago actualizado.")
    return redirect("experiencias:reservas")


@roles_permitidos("admin")
@require_POST
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Inscripcion, pk=pk)
    reserva.delete()
    messages.success(request, "Reserva eliminada.")
    return redirect("experiencias:reservas")

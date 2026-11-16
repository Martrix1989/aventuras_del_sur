from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegistroUsuarioForm, EditarUsuarioForm
from .models import Usuario
from .decorators import roles_permitidos


class AccesoView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("core:home")


@roles_permitidos("admin")
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by("username")
    return render(request, "cuentas/usuarios.html", {"usuarios": usuarios})


@roles_permitidos("admin")
def crear_usuario(request):
    form = RegistroUsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario creado correctamente.")
        return redirect("cuentas:usuarios")
    return render(request, "shared/form.html", {"form": form, "titulo": "Crear usuario", "volver": "cuentas:usuarios"})


@roles_permitidos("admin")
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = EditarUsuarioForm(request.POST or None, instance=usuario)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("cuentas:usuarios")
    return render(request, "shared/form.html", {"form": form, "titulo": "Editar usuario", "volver": "cuentas:usuarios"})


@roles_permitidos("admin")
@require_POST
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propia cuenta desde esta pantalla.")
    else:
        try:
            usuario.delete()
            messages.success(request, "Usuario eliminado.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar: el usuario tiene experiencias creadas. "
                "Puedes desactivarlo desde la opción de editar.",
            )
    return redirect("cuentas:usuarios")

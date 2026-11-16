from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from experiencias.models import Experiencia, Inscripcion


def home(request):
    experiencias = Experiencia.objects.filter(estado=True).select_related("categoria")[:6]
    return render(request, "core/home.html", {"experiencias": experiencias})


@login_required
def dashboard(request):
    user = request.user
    context = {"total_experiencias": 0, "total_reservas": 0, "total_usuarios": 0}
    if user.rol == "admin":
        context["total_experiencias"] = Experiencia.objects.count()
        context["total_reservas"] = Inscripcion.objects.count()
        from cuentas.models import Usuario
        context["total_usuarios"] = Usuario.objects.count()
    elif user.rol == "guia":
        context["total_experiencias"] = Experiencia.objects.filter(creador=user).count()
        context["total_reservas"] = Inscripcion.objects.filter(experiencia__creador=user).count()
    else:
        context["total_reservas"] = Inscripcion.objects.filter(usuario=user).count()
        context["total_experiencias"] = Experiencia.objects.filter(estado=True).count()
    return render(request, "core/dashboard.html", context)

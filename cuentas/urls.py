from django.urls import path
from .views import AccesoView, cerrar_sesion, lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario

app_name = "cuentas"
urlpatterns = [
    path("login/", AccesoView.as_view(), name="login"),
    path("logout/", cerrar_sesion, name="logout"),
    path("usuarios/", lista_usuarios, name="usuarios"),
    path("usuarios/nuevo/", crear_usuario, name="usuario_nuevo"),
    path("usuarios/<int:pk>/editar/", editar_usuario, name="usuario_editar"),
    path("usuarios/<int:pk>/eliminar/", eliminar_usuario, name="usuario_eliminar"),
]

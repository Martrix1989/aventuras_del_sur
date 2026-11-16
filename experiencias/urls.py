from django.urls import path
from . import views

app_name = "experiencias"
urlpatterns = [
    path("", views.lista_experiencias, name="lista"),
    path("nueva/", views.crear_experiencia, name="crear"),
    path("<int:pk>/editar/", views.editar_experiencia, name="editar"),
    path("<int:pk>/eliminar/", views.eliminar_experiencia, name="eliminar"),
    path("categorias/", views.lista_categorias, name="categorias"),
    path("categorias/nueva/", views.crear_categoria, name="categoria_crear"),
    path("categorias/<int:pk>/editar/", views.editar_categoria, name="categoria_editar"),
    path("categorias/<int:pk>/eliminar/", views.eliminar_categoria, name="categoria_eliminar"),
    path("<int:pk>/reservar/", views.reservar_experiencia, name="reservar"),
    path("reservas/", views.mis_reservas, name="reservas"),
    path("reservas/<int:pk>/estado/", views.cambiar_estado_reserva, name="reserva_estado"),
    path("reservas/<int:pk>/eliminar/", views.eliminar_reserva, name="reserva_eliminar"),
    path('mis-reservas', views.mis_reservas,name="mis_reservas"),
]

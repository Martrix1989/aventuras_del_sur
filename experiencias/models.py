from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha_hora = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="experiencias")
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="experiencias_creadas")
    estado = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha_hora", "titulo"]

    def __str__(self):
        return self.titulo

    @property
    def cupos_disponibles(self):
        ocupados = self.inscripciones.count()
        return max(self.cupo_maximo - ocupados, 0)

    @property
    def puede_reservarse(self):
        return self.estado and self.fecha_hora > timezone.now() and self.cupos_disponibles > 0


class Inscripcion(models.Model):
    class EstadosPago(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADO = "confirmado", "Confirmado"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inscripciones")
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=12, choices=EstadosPago.choices, default=EstadosPago.PENDIENTE)

    class Meta:
        ordering = ["-fecha_inscripcion"]
        constraints = [models.UniqueConstraint(fields=["usuario", "experiencia"], name="reserva_unica_por_usuario_experiencia")]

    def __str__(self):
        return f"{self.usuario.username} - {self.experiencia.titulo}"

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Administrador"
        GUIA = "guia", "Guía / Operador"
        TURISTA = "turista", "Turista / Cliente"

    rol = models.CharField(max_length=10, choices=Roles.choices, default=Roles.TURISTA)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = self.Roles.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

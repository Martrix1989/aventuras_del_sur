import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("cuentas", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("descripcion", models.TextField(blank=True)),
                ("activo", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "Categoría", "verbose_name_plural": "Categorías", "ordering": ["nombre"]},
        ),
        migrations.CreateModel(
            name="Experiencia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=150)),
                ("descripcion", models.TextField()),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ("cupo_maximo", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("fecha_hora", models.DateTimeField()),
                ("estado", models.BooleanField(default=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="experiencias", to="experiencias.categoria")),
                ("creador", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="experiencias_creadas", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["fecha_hora", "titulo"]},
        ),
        migrations.CreateModel(
            name="Inscripcion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_inscripcion", models.DateTimeField(auto_now_add=True)),
                ("estado_pago", models.CharField(choices=[("pendiente", "Pendiente"), ("confirmado", "Confirmado")], default="pendiente", max_length=12)),
                ("experiencia", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inscripciones", to="experiencias.experiencia")),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inscripciones", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-fecha_inscripcion"]},
        ),
        migrations.AddConstraint(model_name="inscripcion", constraint=models.UniqueConstraint(fields=("usuario", "experiencia"), name="reserva_unica_por_usuario_experiencia")),
    ]

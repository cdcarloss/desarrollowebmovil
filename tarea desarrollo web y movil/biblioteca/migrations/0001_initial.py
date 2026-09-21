from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Autor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("nacionalidad", models.CharField(max_length=80)),
            ],
            options={"ordering": ["nombre"], "verbose_name": "autor", "verbose_name_plural": "autores"},
        ),
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=80, unique=True)),
                ("descripcion", models.TextField(blank=True)),
            ],
            options={"ordering": ["nombre"], "verbose_name": "categoria", "verbose_name_plural": "categorias"},
        ),
        migrations.CreateModel(
            name="Socio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("correo", models.EmailField(max_length=254, unique=True)),
                ("telefono", models.CharField(max_length=20)),
                ("fecha_registro", models.DateField(auto_now_add=True)),
            ],
            options={"ordering": ["nombre"], "verbose_name": "socio", "verbose_name_plural": "socios"},
        ),
        migrations.CreateModel(
            name="Libro",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=180)),
                ("isbn", models.CharField(max_length=17, unique=True)),
                ("anio_publicacion", models.PositiveIntegerField()),
                ("ejemplares_disponibles", models.PositiveIntegerField(default=1)),
                ("autor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="libros", to="biblioteca.autor")),
                ("categorias", models.ManyToManyField(related_name="libros", to="biblioteca.categoria")),
            ],
            options={"ordering": ["titulo"], "verbose_name": "libro", "verbose_name_plural": "libros"},
        ),
        migrations.CreateModel(
            name="Prestamo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_prestamo", models.DateField(default=django.utils.timezone.now)),
                ("fecha_devolucion", models.DateField(blank=True, null=True)),
                ("devuelto", models.BooleanField(default=False)),
                ("libro", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="prestamos", to="biblioteca.libro")),
                ("socio", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="prestamos", to="biblioteca.socio")),
            ],
            options={"ordering": ["-fecha_prestamo"], "verbose_name": "prestamo", "verbose_name_plural": "prestamos"},
        ),
    ]

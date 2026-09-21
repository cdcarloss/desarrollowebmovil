from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Autor(models.Model):
    nombre = models.CharField(max_length=120)
    nacionalidad = models.CharField(max_length=80)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=180)
    isbn = models.CharField(max_length=17, unique=True)
    anio_publicacion = models.PositiveIntegerField()
    ejemplares_disponibles = models.PositiveIntegerField(default=1)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name="libros")
    categorias = models.ManyToManyField(Categoria, related_name="libros")

    class Meta:
        ordering = ["titulo"]
        verbose_name = "libro"
        verbose_name_plural = "libros"

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.anio_publicacion > timezone.now().year:
            raise ValidationError({"anio_publicacion": "El ano no puede ser futuro."})


class Socio(models.Model):
    nombre = models.CharField(max_length=120)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "socio"
        verbose_name_plural = "socios"

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name="prestamos")
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="prestamos")
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha_prestamo"]
        verbose_name = "prestamo"
        verbose_name_plural = "prestamos"

    def __str__(self):
        return f"{self.libro} - {self.socio}"

    def clean(self):
        if self.fecha_devolucion and self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError({"fecha_devolucion": "La devolucion no puede ser anterior al prestamo."})
        if self.devuelto and not self.fecha_devolucion:
            raise ValidationError({"fecha_devolucion": "Un prestamo devuelto necesita fecha de devolucion."})

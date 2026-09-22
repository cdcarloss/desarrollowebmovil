from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models, transaction
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


def ruta_portada(instance, nombre_archivo):
    """Organiza las imágenes subidas en media/portadas/<libros|juegos>/."""
    carpeta = "libros" if isinstance(instance, Libro) else "juegos"
    return f"portadas/{carpeta}/{nombre_archivo}"


class Prestable(models.Model):
    """Campos y comportamiento comunes a todo lo que la biblioteca presta.

    Es una clase ABSTRACTA (Meta.abstract = True): no crea su propia tabla.
    Django copia "stock" (ejemplares disponibles), "imagen" y estos dos
    métodos dentro de cada modelo concreto que hereda de ella (Libro y
    JuegoMesa), así se evita repetir la lógica de descontar/reponer
    ejemplares y el campo de portada.
    """

    stock = models.PositiveIntegerField("ejemplares disponibles", default=0)
    imagen = models.ImageField("portada", upload_to=ruta_portada, blank=True, null=True)

    class Meta:
        abstract = True

    def descontar_stock(self, cantidad=1):
        self.stock -= cantidad
        self.save(update_fields=["stock"])

    def reponer_stock(self, cantidad=1):
        self.stock += cantidad
        self.save(update_fields=["stock"])


class LibroQuerySet(models.QuerySet):
    """Consultas reutilizables sobre libros (asi las vistas no arman filtros)."""

    def con_stock(self):
        return self.filter(stock__gt=0)

    def de_autor(self, autor_id):
        return self.filter(autor_id=autor_id)

    def de_tipo(self, tipo):
        return self.filter(tipo=tipo)


class Libro(Prestable):
    """El SUPER TIPO: toda fila de esta tabla es un libro, sea fisico o ebook.

    LibroFisico y LibroEbook heredan de Libro usando herencia de tablas de
    Django (multi-table inheritance): cada uno vive en su propia tabla con
    sus columnas propias, unida a esta por una clave primaria compartida.
    El campo "tipo" permite saber cual es cual sin ir a revisar las tablas hijas.
    """

    class Tipo(models.TextChoices):
        FISICO = "FISICO", "Físico"
        EBOOK = "EBOOK", "Ebook"

    titulo = models.CharField("título", max_length=180)
    isbn = models.CharField(
        "ISBN",
        max_length=17,
        unique=True,
        validators=[RegexValidator(r"^[0-9-]{10,17}$", "El ISBN solo admite números y guiones (10 a 17 caracteres).")],
    )
    anio_publicacion = models.PositiveIntegerField(
        "año de publicación", validators=[MinValueValidator(1450)]
    )
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name="libros")
    tipo = models.CharField(max_length=10, choices=Tipo.choices, editable=False)

    objects = LibroQuerySet.as_manager()

    class Meta:
        ordering = ["titulo"]
        verbose_name = "libro"
        verbose_name_plural = "libros"

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

    def clean(self):
        if self.anio_publicacion and self.anio_publicacion > timezone.now().year:
            raise ValidationError({"anio_publicacion": "El año no puede ser futuro."})


class LibroFisico(Libro):
    """Subtipo con ejemplares en papel: importa saber dónde está en la estantería."""

    ubicacion = models.CharField(
        "ubicación en estantería", max_length=40, validators=[MinLengthValidator(2)]
    )

    class Meta:
        verbose_name = "libro físico"
        verbose_name_plural = "libros físicos"

    def save(self, *args, **kwargs):
        self.tipo = Libro.Tipo.FISICO
        super().save(*args, **kwargs)


class LibroEbook(Libro):
    """Subtipo digital: agrega el formato de archivo y el tamaño de descarga."""

    class Formato(models.TextChoices):
        EPUB = "EPUB", "EPUB"
        PDF = "PDF", "PDF"
        MOBI = "MOBI", "MOBI"

    formato_archivo = models.CharField(max_length=10, choices=Formato.choices, default=Formato.EPUB)
    tamano_mb = models.PositiveIntegerField("tamaño (MB)", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "ebook"
        verbose_name_plural = "ebooks"

    def save(self, *args, **kwargs):
        self.tipo = Libro.Tipo.EBOOK
        super().save(*args, **kwargs)


class JuegoMesa(Prestable):
    """Tabla independiente: un juego de mesa NO es un subtipo de Libro."""

    class Categoria(models.TextChoices):
        ESTRATEGIA = "ESTRATEGIA", "Estrategia"
        FAMILIAR = "FAMILIAR", "Familiar"
        PARTY = "PARTY", "Party"
        INFANTIL = "INFANTIL", "Infantil"

    nombre = models.CharField(max_length=120)
    marca = models.CharField("marca / editorial", max_length=80)
    categoria = models.CharField(max_length=12, choices=Categoria.choices)
    jugadores_min = models.PositiveSmallIntegerField("jugadores (mínimo)", validators=[MinValueValidator(1)])
    jugadores_max = models.PositiveSmallIntegerField("jugadores (máximo)", validators=[MinValueValidator(1)])
    edad_minima = models.PositiveSmallIntegerField("edad mínima")

    class Meta:
        ordering = ["nombre"]
        verbose_name = "juego de mesa"
        verbose_name_plural = "juegos de mesa"

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.jugadores_min and self.jugadores_max and self.jugadores_min > self.jugadores_max:
            raise ValidationError({"jugadores_max": "Debe ser mayor o igual que el mínimo de jugadores."})


class Socio(models.Model):
    nombre = models.CharField(max_length=120, validators=[MinLengthValidator(3)])
    correo = models.EmailField("correo electrónico", unique=True)
    telefono = models.CharField(
        "teléfono",
        max_length=15,
        validators=[RegexValidator(r"^\+?\d{8,12}$", "Ingresa un teléfono válido, por ejemplo +56912345678.")],
    )
    fecha_registro = models.DateField(auto_now_add=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="socio",
        help_text="Cuenta con la que este socio inicia sesión (opcional). Permite que vea sus propios préstamos.",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "socio"
        verbose_name_plural = "socios"

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    """Datos de presentación de una cuenta (foto, descripción corta).

    Se guarda aparte de auth.User porque ese modelo lo trae Django y no
    se puede modificar directamente. Cada usuario tiene exactamente un
    Perfil: se crea solo, mediante una señal, apenas se crea la cuenta
    (ver signals.py), así ninguna vista tiene que acordarse de crearlo.
    """

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    foto = models.ImageField("foto de perfil", upload_to="perfiles/", blank=True, null=True)
    descripcion = models.CharField("descripción", max_length=280, blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Comentario(models.Model):
    """Una opinión de un usuario sobre un libro: el "foro" del catálogo."""

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios")
    texto = models.TextField(
        "opinión",
        validators=[MinLengthValidator(5, "La opinión debe tener al menos 5 caracteres.")],
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha"]
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"

    def __str__(self):
        return f"{self.usuario} sobre {self.libro}"


class Empleado(models.Model):
    class Cargo(models.TextChoices):
        BIBLIOTECARIO = "BIBLIOTECARIO", "Bibliotecario/a"
        ASISTENTE = "ASISTENTE", "Asistente"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador/a"

    nombre = models.CharField(max_length=120)
    correo = models.EmailField("correo electrónico", unique=True)
    cargo = models.CharField(max_length=20, choices=Cargo.choices, default=Cargo.ASISTENTE)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "empleado"
        verbose_name_plural = "empleados"

    def __str__(self):
        return f"{self.nombre} ({self.get_cargo_display()})"


class Prestamo(models.Model):
    """Un préstamo es de un libro (físico o ebook, misma tabla Libro) O de
    un juego de mesa, nunca de ambos ni de ninguno. Se usan dos FK
    opcionales y el modelo obliga a que solo una esté llena (ver clean()),
    en vez de una relación genérica (GenericForeignKey), más avanzada de
    lo que pide el curso.

    El plazo de devolución depende del tipo de producto: un ebook se
    presta por menos días que un libro físico, porque no hay que
    trasladarlo. "empleado" queda vacío cuando el propio socio pide el
    préstamo desde el portal (ver carrito.py), y con valor cuando un
    bibliotecario lo registra en el mesón.
    """

    PLAZO_DIAS_FISICO = 14
    PLAZO_DIAS_EBOOK = 7
    PLAZO_DIAS_JUEGO = 10

    libro = models.ForeignKey(
        Libro, on_delete=models.PROTECT, null=True, blank=True, related_name="prestamos"
    )
    juego = models.ForeignKey(
        JuegoMesa, on_delete=models.PROTECT, null=True, blank=True, related_name="prestamos"
    )
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="prestamos")
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="prestamos",
        help_text="Vacío cuando el socio pide el préstamo desde el portal, sin pasar por el mesón.",
    )
    fecha_prestamo = models.DateField(default=timezone.now, editable=False)
    fecha_devolucion_prevista = models.DateField(editable=False)
    fecha_devolucion_real = models.DateField(null=True, blank=True, editable=False)
    devuelto = models.BooleanField(default=False, editable=False)

    class Meta:
        # "-pk" como segundo criterio: fecha_prestamo solo tiene día, no hora,
        # así que dos préstamos del mismo día quedarían "empatados" y el más
        # nuevo podría no mostrarse arriba. Por pk sí hay un orden real.
        ordering = ["-fecha_prestamo", "-pk"]
        verbose_name = "préstamo"
        verbose_name_plural = "préstamos"

    def __str__(self):
        return f"Préstamo #{self.pk}: {self.producto} a {self.socio}"

    @property
    def producto(self):
        """El libro o el juego prestado."""
        return self.libro or self.juego

    @property
    def dias_de_atraso(self):
        if self.devuelto or not self.fecha_devolucion_prevista:
            return 0
        return max((timezone.now().date() - self.fecha_devolucion_prevista).days, 0)

    @property
    def esta_atrasado(self):
        return self.dias_de_atraso > 0

    def clean(self):
        if bool(self.libro_id) == bool(self.juego_id):
            raise ValidationError("Selecciona un libro o un juego de mesa (no ambos, no ninguno).")
        if self.empleado_id and not self.empleado.activo:
            raise ValidationError({"empleado": "El empleado seleccionado está inactivo."})
        if self._state.adding and self.producto and self.producto.stock < 1:
            raise ValidationError(f"No quedan ejemplares disponibles de «{self.producto}».")

    def _plazo_dias(self):
        if self.juego_id:
            return self.PLAZO_DIAS_JUEGO
        return self.PLAZO_DIAS_EBOOK if self.libro.tipo == Libro.Tipo.EBOOK else self.PLAZO_DIAS_FISICO

    def save(self, *args, **kwargs):
        if not self._state.adding:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            Modelo = Libro if self.libro_id else JuegoMesa
            producto = Modelo.objects.select_for_update().get(pk=self.libro_id or self.juego_id)
            if producto.stock < 1:
                raise ValidationError(f"No quedan ejemplares disponibles de «{producto}».")
            if self.libro_id:
                self.libro = producto
            else:
                self.juego = producto
            self.fecha_devolucion_prevista = timezone.now().date() + timedelta(days=self._plazo_dias())
            producto.descontar_stock()
            super().save(*args, **kwargs)

    def marcar_devuelto(self):
        with transaction.atomic():
            Modelo = Libro if self.libro_id else JuegoMesa
            producto = Modelo.objects.select_for_update().get(pk=self.libro_id or self.juego_id)
            producto.reponer_stock()
            self.devuelto = True
            self.fecha_devolucion_real = timezone.now().date()
            self.save(update_fields=["devuelto", "fecha_devolucion_real"])

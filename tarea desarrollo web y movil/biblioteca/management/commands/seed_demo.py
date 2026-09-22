from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from biblioteca.models import Autor, Comentario, Empleado, JuegoMesa, LibroEbook, LibroFisico, Prestamo, Socio


def asignar_imagen_semilla(producto, ruta_estatica):
    """Copia una portada que viaja en static/ hacia el campo "imagen" del
    producto (que vive en MEDIA_ROOT). Solo se hace una vez: si el
    producto ya tiene una portada (por ejemplo, alguien subió una mejor
    desde el formulario), no se pisa."""
    if producto.imagen:
        return
    ruta_absoluta = finders.find(ruta_estatica)
    if not ruta_absoluta:
        return
    with open(ruta_absoluta, "rb") as archivo:
        producto.imagen.save(ruta_estatica.rsplit("/", 1)[-1], File(archivo), save=True)


class Command(BaseCommand):
    help = "Carga usuarios y datos realistas para revisar la aplicación."

    def handle(self, *args, **options):
        self.crear_usuarios()
        autores = self.crear_autores()
        libros_fisicos = self.crear_libros_fisicos(autores)
        libros_ebook = self.crear_libros_ebook(autores)
        juegos = self.crear_juegos()
        socios = self.crear_socios()
        empleados = self.crear_empleados()
        self.crear_prestamos(libros_fisicos, libros_ebook, juegos, socios, empleados)
        self.crear_comentarios(libros_fisicos, libros_ebook, socios)
        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados correctamente."))
        self.stdout.write("Administrador: admin / Admin12345!")
        self.stdout.write("Usuario común: lector / Lector12345!")
        self.stdout.write("Socios (contraseña = inicial del nombre + 12345678):")
        for socio in Socio.objects.exclude(usuario=None).order_by("nombre"):
            self.stdout.write(f"  {socio.usuario.username} / {socio.nombre[0].upper()}12345678")

    def crear_usuarios(self):
        User = get_user_model()
        admin, _ = User.objects.get_or_create(username="admin")
        admin.email = "admin@bibliotecalarecamara.cl"
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("Admin12345!")
        admin.save()
        admin.perfil.descripcion = "Administra el catálogo, los socios y los préstamos de la biblioteca."
        admin.perfil.save()

        lector, _ = User.objects.get_or_create(username="lector")
        lector.email = "lector@bibliotecalarecamara.cl"
        lector.set_password("Lector12345!")
        lector.save()
        lector.perfil.descripcion = "Cuenta de prueba genérica (sin socio vinculado)."
        lector.perfil.save()

    def crear_autores(self):
        datos = [
            ("Gabriel García Márquez", "Colombia"),
            ("Isabel Allende", "Chile"),
            ("Julio Cortázar", "Argentina"),
            ("Jane Austen", "Reino Unido"),
            ("George Orwell", "Reino Unido"),
            ("Roberto Bolaño", "Chile"),
        ]
        return {
            nombre: Autor.objects.get_or_create(nombre=nombre, defaults={"nacionalidad": pais})[0]
            for nombre, pais in datos
        }

    def crear_libros_fisicos(self, autores):
        # (titulo, isbn, año, stock, ubicación, autor, imagen semilla)
        datos = [
            ("Cien años de soledad", "9780307474728", 1967, 3, "Estante A-01", "Gabriel García Márquez", "cien-anos-de-soledad.jpg"),
            ("El amor en los tiempos del cólera", "9780307389732", 1985, 2, "Estante A-02", "Gabriel García Márquez", "el-amor-en-los-tiempos-del-colera.jpg"),
            ("La casa de los espíritus", "9781501117015", 1982, 2, "Estante A-03", "Isabel Allende", "la-casa-de-los-espiritus.jpg"),
            ("Rayuela", "9788437604572", 1963, 1, "Estante B-01", "Julio Cortázar", "rayuela.jpg"),
            ("Orgullo y prejuicio", "9780141439518", 1813, 4, "Estante C-01", "Jane Austen", "orgullo-y-prejuicio.jpg"),
            ("1984", "9780451524935", 1949, 5, "Estante D-01", "George Orwell", "1984.jpg"),
            ("Rebelión en la granja", "9780451526342", 1945, 3, "Estante D-02", "George Orwell", "rebelion-en-la-granja.jpg"),
            ("Los detectives salvajes", "9788433974787", 1998, 1, "Estante B-02", "Roberto Bolaño", "los-detectives-salvajes.jpg"),
        ]
        libros = {}
        for titulo, isbn, anio, stock, ubicacion, autor, imagen in datos:
            libro, _ = LibroFisico.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo,
                    "anio_publicacion": anio,
                    "stock": stock,
                    "ubicacion": ubicacion,
                    "autor": autores[autor],
                },
            )
            asignar_imagen_semilla(libro, f"biblioteca/img/semillas/libros/{imagen}")
            libros[isbn] = libro
        return libros

    def crear_libros_ebook(self, autores):
        # (titulo, isbn, año, formato, tamaño MB, autor, imagen semilla)
        datos = [
            ("Cien años de soledad (ebook)", "9780307474711", 1967, "EPUB", 3, "Gabriel García Márquez", "cien-anos-de-soledad-ebook.jpg"),
            ("Paula", "9780061564253", 1994, "EPUB", 2, "Isabel Allende", "paula.jpg"),
            ("Bestiario", "9788420633121", 1951, "PDF", 4, "Julio Cortázar", "bestiario.jpg"),
            ("Emma", "9780141439587", 1815, "MOBI", 3, "Jane Austen", "emma.jpg"),
            ("Rayuela (ebook)", "9990000004", 1963, "EPUB", 5, "Julio Cortázar", "rayuela-ebook.jpg"),
            ("Rebelión en la granja (ebook)", "9990000007", 1945, "EPUB", 5, "George Orwell", "rebelion-en-la-granja-ebook.jpg"),
        ]
        libros = {}
        for titulo, isbn, anio, formato, tamano, autor, imagen in datos:
            libro, _ = LibroEbook.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo,
                    "anio_publicacion": anio,
                    "stock": 99,
                    "formato_archivo": formato,
                    "tamano_mb": tamano,
                    "autor": autores[autor],
                },
            )
            asignar_imagen_semilla(libro, f"biblioteca/img/semillas/libros/{imagen}")
            libros[isbn] = libro
        return libros

    def crear_juegos(self):
        # (nombre, marca, categoria, jugadores min, max, edad, stock, imagen semilla)
        datos = [
            ("Catan", "Devir", JuegoMesa.Categoria.ESTRATEGIA, 3, 4, 10, 2, "catan.jpg"),
            ("Carcassonne", "Devir", JuegoMesa.Categoria.FAMILIAR, 2, 5, 7, 2, "carcassonne.jpg"),
            ("Dixit", "Libellud", JuegoMesa.Categoria.PARTY, 3, 6, 8, 1, "dixit.jpg"),
            ("Catan: Los Colonos Junior", "Devir", JuegoMesa.Categoria.INFANTIL, 2, 4, 6, 2, "catan-los-colonos-junior.jpg"),
            ("Azul", "Next Move Games", JuegoMesa.Categoria.ESTRATEGIA, 2, 4, 8, 1, "azul.jpg"),
        ]
        juegos = {}
        for nombre, marca, categoria, jmin, jmax, edad, stock, imagen in datos:
            juego, _ = JuegoMesa.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "marca": marca,
                    "categoria": categoria,
                    "jugadores_min": jmin,
                    "jugadores_max": jmax,
                    "edad_minima": edad,
                    "stock": stock,
                },
            )
            asignar_imagen_semilla(juego, f"biblioteca/img/semillas/juegos/{imagen}")
            juegos[nombre] = juego
        return juegos

    def crear_socios(self):
        User = get_user_model()
        datos = [
            ("Sofía Martínez", "sofia.martinez@example.com", "+56911112222"),
            ("Mateo González", "mateo.gonzalez@example.com", "+56922223333"),
            ("Valentina Rojas", "valentina.rojas@example.com", "+56933334444"),
            ("Diego Fuentes", "diego.fuentes@example.com", "+56944445555"),
            ("Camila Torres", "camila.torres@example.com", "+56955556666"),
        ]
        socios = {}
        for nombre, correo, tel in datos:
            socio, _ = Socio.objects.get_or_create(correo=correo, defaults={"nombre": nombre, "telefono": tel})
            if not socio.usuario_id:
                # Contraseña genérica de bienvenida: la inicial del nombre
                # más un relleno fijo. Es una contraseña de demostración,
                # pensada para que cada socio pueda entrar y cambiarla.
                username = slugify(nombre)
                inicial = nombre[0].upper()
                usuario, _ = User.objects.get_or_create(username=username, defaults={"email": correo})
                usuario.first_name = nombre.split()[0]
                usuario.set_password(f"{inicial}12345678")
                usuario.save()
                socio.usuario = usuario
                socio.save(update_fields=["usuario"])
            socios[correo] = socio
        return socios

    def crear_empleados(self):
        datos = [
            ("Andrea Silva", "andrea.silva@bibliotecalarecamara.cl", Empleado.Cargo.ADMINISTRADOR),
            ("Felipe Muñoz", "felipe.munoz@bibliotecalarecamara.cl", Empleado.Cargo.BIBLIOTECARIO),
            ("Javiera Pérez", "javiera.perez@bibliotecalarecamara.cl", Empleado.Cargo.ASISTENTE),
        ]
        return {
            correo: Empleado.objects.get_or_create(correo=correo, defaults={"nombre": nombre, "cargo": cargo})[0]
            for nombre, correo, cargo in datos
        }

    def crear_prestamos(self, libros_fisicos, libros_ebook, juegos, socios, empleados):
        if Prestamo.objects.exists():
            return
        felipe = empleados["felipe.munoz@bibliotecalarecamara.cl"]
        javiera = empleados["javiera.perez@bibliotecalarecamara.cl"]
        andrea = empleados["andrea.silva@bibliotecalarecamara.cl"]

        # Prestamos registrados en el mesón (con empleado)
        prestamos_mesa = [
            ("9780307474728", "sofia.martinez@example.com", felipe),
            ("9781501117015", "mateo.gonzalez@example.com", felipe),
            ("9780451524935", "valentina.rojas@example.com", javiera),
            ("9788433974787", "diego.fuentes@example.com", andrea),
        ]
        for isbn, correo, empleado in prestamos_mesa:
            Prestamo.objects.create(libro=libros_fisicos[isbn], socio=socios[correo], empleado=empleado)

        # Prestamos pedidos por el propio socio desde su lista (sin empleado)
        prestamos_portal = [
            ("9780307474711", "camila.torres@example.com"),
            ("9788420633121", "sofia.martinez@example.com"),
        ]
        for isbn, correo in prestamos_portal:
            Prestamo.objects.create(libro=libros_ebook[isbn], socio=socios[correo])

        Prestamo.objects.create(juego=juegos["Catan"], socio=socios["mateo.gonzalez@example.com"], empleado=felipe)
        Prestamo.objects.create(juego=juegos["Dixit"], socio=socios["valentina.rojas@example.com"])

        # Uno ya devuelto, para mostrar ese estado en el listado.
        devuelto = Prestamo.objects.create(
            libro=libros_fisicos["9780141439518"], socio=socios["diego.fuentes@example.com"], empleado=javiera
        )
        devuelto.marcar_devuelto()

        # Uno vencido hace unos días, para mostrar el aviso de atraso.
        atrasado = Prestamo.objects.create(
            libro=libros_fisicos["9780451526342"], socio=socios["camila.torres@example.com"], empleado=andrea
        )
        hoy = timezone.now().date()
        Prestamo.objects.filter(pk=atrasado.pk).update(
            fecha_prestamo=hoy - timedelta(days=20),
            fecha_devolucion_prevista=hoy - timedelta(days=6),
        )

    def crear_comentarios(self, libros_fisicos, libros_ebook, socios):
        if Comentario.objects.exists():
            return
        datos = [
            ("9780307474728", "sofia.martinez@example.com", "Una relectura obligada. Cada vez encuentro algo nuevo en Macondo."),
            ("9780307474728", "mateo.gonzalez@example.com", "Al principio cuesta seguir a toda la familia Buendía, pero vale la pena."),
            ("9780451524935", "valentina.rojas@example.com", "Inquietante y todavía muy vigente. Lo terminé en dos días."),
            ("9788433974787", "diego.fuentes@example.com", "Bolaño construye personajes que se sienten reales. Muy recomendado."),
            ("9780141439518", "camila.torres@example.com", "Elizabeth Bennet es uno de mis personajes favoritos de la literatura."),
        ]
        for isbn, correo, texto in datos:
            socio = socios[correo]
            if not socio.usuario_id:
                continue
            Comentario.objects.get_or_create(
                libro=libros_fisicos[isbn], usuario=socio.usuario, defaults={"texto": texto}
            )

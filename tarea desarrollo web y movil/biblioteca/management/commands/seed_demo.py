from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from biblioteca.models import Autor, Categoria, Libro, Prestamo, Socio


class Command(BaseCommand):
    help = "Carga usuarios y datos realistas para revisar la aplicacion localmente."

    def handle(self, *args, **options):
        user_model = get_user_model()
        admin, _ = user_model.objects.get_or_create(username="admin")
        admin.email = "admin@bibliotecahorizonte.local"
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("Admin12345!")
        admin.save()

        lector, _ = user_model.objects.get_or_create(username="lector")
        lector.email = "lector@bibliotecahorizonte.local"
        lector.set_password("Lector12345!")
        lector.save()

        autores = [
            ("Gabriel Garcia Marquez", "Colombia"),
            ("Isabel Allende", "Chile"),
            ("Julio Cortazar", "Argentina"),
            ("Jane Austen", "Reino Unido"),
            ("George Orwell", "Reino Unido"),
        ]
        autor_map = {}
        for nombre, nacionalidad in autores:
            autor_map[nombre], _ = Autor.objects.get_or_create(nombre=nombre, defaults={"nacionalidad": nacionalidad})

        categorias = ["Novela", "Realismo magico", "Ciencia ficcion", "Clasicos", "Ensayo"]
        categoria_map = {nombre: Categoria.objects.get_or_create(nombre=nombre)[0] for nombre in categorias}

        libros = [
            ("Cien anos de soledad", "9780307474728", 1967, "Gabriel Garcia Marquez", ["Novela", "Realismo magico"]),
            ("El amor en los tiempos del colera", "9780307389732", 1985, "Gabriel Garcia Marquez", ["Novela"]),
            ("La casa de los espiritus", "9781501117015", 1982, "Isabel Allende", ["Novela", "Realismo magico"]),
            ("Rayuela", "9788437604562", 1963, "Julio Cortazar", ["Novela", "Clasicos"]),
            ("Final del juego", "9788420633134", 1956, "Julio Cortazar", ["Novela"]),
            ("Orgullo y prejuicio", "9780141439518", 1813, "Jane Austen", ["Clasicos", "Novela"]),
            ("Emma", "9780141439587", 1815, "Jane Austen", ["Clasicos", "Novela"]),
            ("1984", "9780451524935", 1949, "George Orwell", ["Ciencia ficcion", "Clasicos"]),
            ("Rebelion en la granja", "9780451526342", 1945, "George Orwell", ["Novela", "Clasicos"]),
            ("Notas sobre literatura", "9788420429126", 1998, "Isabel Allende", ["Ensayo"]),
        ]
        libro_map = {}
        for titulo, isbn, anio, autor, nombres_categorias in libros:
            libro, _ = Libro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo,
                    "anio_publicacion": anio,
                    "ejemplares_disponibles": 3,
                    "autor": autor_map[autor],
                },
            )
            libro_map[isbn] = libro
            libro.categorias.set([categoria_map[nombre] for nombre in nombres_categorias])

        socios = [
            ("Sofia Martinez", "sofia.martinez@example.com", "+56911112222"),
            ("Mateo Gonzalez", "mateo.gonzalez@example.com", "+56922223333"),
            ("Valentina Rojas", "valentina.rojas@example.com", "+56933334444"),
            ("Diego Fuentes", "diego.fuentes@example.com", "+56944445555"),
            ("Camila Torres", "camila.torres@example.com", "+56955556666"),
        ]
        socio_map = {}
        for nombre, correo, telefono in socios:
            socio_map[correo], _ = Socio.objects.get_or_create(
                correo=correo,
                defaults={"nombre": nombre, "telefono": telefono},
            )

        prestamos = [
            ("9780307474728", "sofia.martinez@example.com"),
            ("9781501117015", "mateo.gonzalez@example.com"),
            ("9780451524935", "valentina.rojas@example.com"),
        ]
        for isbn, correo in prestamos:
            Prestamo.objects.get_or_create(libro=libro_map[isbn], socio=socio_map[correo])

        self.stdout.write(self.style.SUCCESS("Datos de demostracion cargados correctamente."))
        self.stdout.write("Usuario administrador: admin / Admin12345!")
        self.stdout.write("Usuario comun: lector / Lector12345!")

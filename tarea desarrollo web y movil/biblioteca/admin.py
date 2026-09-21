from django.contrib import admin

from .models import Autor, Categoria, Libro, Prestamo, Socio


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "isbn", "autor", "anio_publicacion", "ejemplares_disponibles")
    list_filter = ("autor", "categorias", "anio_publicacion")
    search_fields = ("titulo", "isbn", "autor__nombre")
    ordering = ("titulo",)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("libro", "socio", "fecha_prestamo", "fecha_devolucion", "devuelto")
    list_filter = ("devuelto", "fecha_prestamo")
    search_fields = ("libro__titulo", "socio__nombre", "socio__correo")
    ordering = ("-fecha_prestamo",)


admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Socio)

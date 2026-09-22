from django.contrib import admin

from .models import Autor, Comentario, Empleado, JuegoMesa, LibroEbook, LibroFisico, Perfil, Prestamo, Socio


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nacionalidad")
    list_filter = ("nacionalidad",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(LibroFisico)
class LibroFisicoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "isbn", "ubicacion", "stock")
    list_filter = ("autor", "anio_publicacion")
    list_editable = ("stock",)
    search_fields = ("titulo", "isbn", "autor__nombre")
    ordering = ("titulo",)


@admin.register(LibroEbook)
class LibroEbookAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "isbn", "formato_archivo", "tamano_mb", "stock")
    list_filter = ("autor", "formato_archivo")
    list_editable = ("stock",)
    search_fields = ("titulo", "isbn", "autor__nombre")
    ordering = ("titulo",)


@admin.register(JuegoMesa)
class JuegoMesaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "marca", "categoria", "jugadores_min", "jugadores_max", "stock")
    list_filter = ("categoria", "marca")
    list_editable = ("stock",)
    search_fields = ("nombre", "marca")
    ordering = ("nombre",)


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono", "usuario", "fecha_registro")
    list_filter = ("fecha_registro",)
    search_fields = ("nombre", "correo")
    ordering = ("nombre",)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cargo", "correo", "activo")
    list_filter = ("cargo", "activo")
    list_editable = ("activo",)
    search_fields = ("nombre", "correo")
    ordering = ("nombre",)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "socio", "empleado", "fecha_prestamo", "fecha_devolucion_prevista", "devuelto")
    list_filter = ("devuelto", "empleado", "fecha_prestamo")
    search_fields = ("libro__titulo", "juego__nombre", "socio__nombre")
    readonly_fields = ("fecha_prestamo", "fecha_devolucion_prevista", "fecha_devolucion_real", "devuelto")
    ordering = ("-fecha_prestamo",)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "descripcion")
    search_fields = ("usuario__username",)
    ordering = ("usuario__username",)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("libro", "usuario", "fecha")
    list_filter = ("fecha",)
    search_fields = ("texto", "usuario__username", "libro__titulo")
    ordering = ("-fecha",)

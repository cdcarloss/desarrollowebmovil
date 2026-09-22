from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.BibliotecaLoginView.as_view(), name="login"),
    path("logout/", views.BibliotecaLogoutView.as_view(), name="logout"),

    path("libros/", views.libro_list, name="libro_list"),
    path("libros/nuevo/<str:tipo>/", views.libro_create, name="libro_create"),
    path("libros/<int:pk>/", views.libro_detalle, name="libro_detalle"),
    path("libros/<int:pk>/editar/", views.libro_update, name="libro_update"),
    path("libros/<int:pk>/eliminar/", views.libro_delete, name="libro_delete"),

    path("juegos/", views.juego_list, name="juego_list"),
    path("juegos/nuevo/", views.juego_create, name="juego_create"),
    path("juegos/<int:pk>/editar/", views.juego_update, name="juego_update"),
    path("juegos/<int:pk>/eliminar/", views.juego_delete, name="juego_delete"),

    path("socios/", views.socio_list, name="socio_list"),
    path("socios/nuevo/", views.socio_create, name="socio_create"),
    path("socios/<int:pk>/editar/", views.socio_update, name="socio_update"),
    path("socios/<int:pk>/eliminar/", views.socio_delete, name="socio_delete"),

    path("prestamos/", views.prestamo_list, name="prestamo_list"),
    path("prestamos/nuevo/", views.prestamo_create, name="prestamo_create"),
    path("prestamos/<int:pk>/editar/", views.prestamo_update, name="prestamo_update"),
    path("prestamos/<int:pk>/eliminar/", views.prestamo_delete, name="prestamo_delete"),
    path("prestamos/<int:pk>/devolver/", views.prestamo_devolver, name="prestamo_devolver"),

    path("mi-lista/", views.carrito_ver, name="carrito_ver"),
    path("mi-lista/agregar/<str:tipo>/<int:pk>/", views.carrito_agregar, name="carrito_agregar"),
    path("mi-lista/quitar/<str:clave>/", views.carrito_quitar, name="carrito_quitar"),
    path("mi-lista/confirmar/", views.checkout, name="checkout"),

    path("mis-prestamos/", views.mis_prestamos, name="mis_prestamos"),
    path("perfil/", views.perfil_editar, name="perfil_editar"),
]

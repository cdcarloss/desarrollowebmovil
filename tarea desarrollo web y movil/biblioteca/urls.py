from django.urls import path

from .views import (
    BibliotecaLoginView,
    BibliotecaLogoutView,
    home,
    libro_create,
    libro_delete,
    libro_list,
    libro_update,
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", BibliotecaLoginView.as_view(), name="login"),
    path("logout/", BibliotecaLogoutView.as_view(), name="logout"),
    path("libros/", libro_list, name="libro_list"),
    path("libros/nuevo/", libro_create, name="libro_create"),
    path("libros/<int:pk>/editar/", libro_update, name="libro_update"),
    path("libros/<int:pk>/eliminar/", libro_delete, name="libro_delete"),
]

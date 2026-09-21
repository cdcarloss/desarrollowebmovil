from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LibroForm, LoginForm
from .models import Categoria, Libro


class BibliotecaLoginView(LoginView):
    template_name = "biblioteca/login.html"
    authentication_form = LoginForm


class BibliotecaLogoutView(LogoutView):
    pass


@login_required
def home(request):
    context = {
        "total_libros": Libro.objects.count(),
        "total_categorias": Categoria.objects.count(),
    }
    return render(request, "biblioteca/home.html", context)


@login_required
def libro_list(request):
    libros = Libro.objects.select_related("autor").prefetch_related("categorias")
    categoria_id = request.GET.get("categoria")
    if categoria_id:
        libros = libros.filter(categorias__id=categoria_id)
    context = {
        "libros": libros,
        "categorias": Categoria.objects.all(),
        "categoria_seleccionada": categoria_id,
    }
    return render(request, "biblioteca/libro_list.html", context)


@login_required
def libro_create(request):
    form = LibroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("libro_list")
    return render(request, "biblioteca/libro_form.html", {"form": form, "accion": "Crear"})


@login_required
def libro_update(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    form = LibroForm(request.POST or None, instance=libro)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("libro_list")
    return render(request, "biblioteca/libro_form.html", {"form": form, "accion": "Editar"})


@login_required
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        libro.delete()
        return redirect("libro_list")
    return render(request, "biblioteca/libro_confirm_delete.html", {"libro": libro})

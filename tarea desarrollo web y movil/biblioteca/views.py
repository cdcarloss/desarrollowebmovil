from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.db.models import Prefetch, ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from . import carrito
from .forms import (
    ComentarioForm,
    JuegoMesaForm,
    LibroEbookForm,
    LibroFisicoForm,
    LoginForm,
    PerfilForm,
    PrestamoEditForm,
    PrestamoForm,
    SocioForm,
)
from .models import Autor, Empleado, JuegoMesa, Libro, LibroEbook, LibroFisico, Perfil, Prestamo, Socio

# Une cada tipo de libro con su formulario, su modelo y una etiqueta para
# los mensajes y titulos. Vive aqui (y no en el modelo) porque es una
# decision de la capa de presentacion: que formulario mostrar segun la URL.
FORMULARIOS_LIBRO = {
    Libro.Tipo.FISICO: (LibroFisicoForm, LibroFisico, "libro físico"),
    Libro.Tipo.EBOOK: (LibroEbookForm, LibroEbook, "ebook"),
}


def solo_administradores(vista):
    """Como @login_required, pero además exige user.is_staff.

    Se usa en las vistas de gestión (catálogo, socios, préstamos): un
    socio con sesión iniciada puede navegar y pedir préstamos, pero no
    crear/editar/eliminar ni ver los datos de otros socios. is_staff ya
    viene con django.contrib.auth, así que no hace falta inventar un
    campo de "rol" propio.
    """

    @wraps(vista)
    @login_required
    def envoltura(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Esa sección es solo para administradores de la biblioteca.")
            return redirect("home")
        return vista(request, *args, **kwargs)

    return envoltura


class BibliotecaLoginView(LoginView):
    template_name = "biblioteca/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class BibliotecaLogoutView(LogoutView):
    pass


@login_required
def home(request):
    context = {
        "libros_destacados": Libro.objects.con_stock().select_related("autor")[:4],
        "juegos_destacados": JuegoMesa.objects.filter(stock__gt=0)[:4],
        "total_libros": Libro.objects.count(),
        "total_juegos": JuegoMesa.objects.count(),
        "total_socios": Socio.objects.count(),
        "total_prestamos": Prestamo.objects.filter(devuelto=False).count(),
    }
    return render(request, "biblioteca/home.html", context)


@login_required
def libro_list(request):
    autor_id = request.GET.get("autor", "")
    tipo = request.GET.get("tipo", "")
    libros = Libro.objects.select_related("autor")
    error = None

    if autor_id.isdigit():
        libros = libros.de_autor(int(autor_id))
    elif autor_id:
        error = "El filtro de autor no es válido."
        libros = libros.none()

    if tipo and tipo in Libro.Tipo.values:
        libros = libros.de_tipo(tipo)
    elif tipo:
        error = "El filtro de formato no es válido."
        libros = libros.none()

    if request.user.is_staff:
        # Solo el administrador ve quién tiene cada ejemplar prestado, asi
        # que solo para el se trae ese dato (evita la consulta si nadie la va a usar).
        libros = libros.prefetch_related(
            Prefetch(
                "prestamos",
                queryset=Prestamo.objects.filter(devuelto=False).select_related("socio"),
                to_attr="prestamos_activos",
            )
        )

    context = {
        "libros": libros,
        "autores": Autor.objects.all(),
        "tipos": Libro.Tipo.choices,
        "autor_seleccionado": autor_id,
        "tipo_seleccionado": tipo,
        "error": error,
    }
    return render(request, "biblioteca/libro_list.html", context)


@solo_administradores
def libro_create(request, tipo):
    datos_tipo = FORMULARIOS_LIBRO.get(tipo)
    if not datos_tipo:
        raise Http404("Tipo de libro no válido.")
    FormClass, _modelo, etiqueta = datos_tipo
    form = FormClass(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{etiqueta.capitalize()} creado correctamente.")
        return redirect("libro_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": f"Nuevo {etiqueta}", "volver": "libro_list"})


@solo_administradores
def libro_update(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    FormClass, Modelo, etiqueta = FORMULARIOS_LIBRO[libro.tipo]
    instancia = get_object_or_404(Modelo, pk=pk)
    form = FormClass(request.POST or None, request.FILES or None, instance=instancia)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{etiqueta.capitalize()} actualizado correctamente.")
        return redirect("libro_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": f"Editar {etiqueta}", "volver": "libro_list"})


@solo_administradores
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        try:
            libro.delete()
            messages.success(request, "Libro eliminado.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: el libro tiene préstamos registrados.")
        return redirect("libro_list")
    return render(
        request,
        "biblioteca/confirm_delete.html",
        {"objeto": libro, "tipo": "libro", "volver": "libro_list"},
    )


@login_required
def juego_list(request):
    juegos = JuegoMesa.objects.all()
    if request.user.is_staff:
        juegos = juegos.prefetch_related(
            Prefetch(
                "prestamos",
                queryset=Prestamo.objects.filter(devuelto=False).select_related("socio"),
                to_attr="prestamos_activos",
            )
        )
    return render(request, "biblioteca/juego_list.html", {"juegos": juegos})


@solo_administradores
def juego_create(request):
    form = JuegoMesaForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Juego de mesa creado correctamente.")
        return redirect("juego_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": "Nuevo juego de mesa", "volver": "juego_list"})


@solo_administradores
def juego_update(request, pk):
    juego = get_object_or_404(JuegoMesa, pk=pk)
    form = JuegoMesaForm(request.POST or None, request.FILES or None, instance=juego)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Juego de mesa actualizado correctamente.")
        return redirect("juego_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": "Editar juego de mesa", "volver": "juego_list"})


@solo_administradores
def juego_delete(request, pk):
    juego = get_object_or_404(JuegoMesa, pk=pk)
    if request.method == "POST":
        try:
            juego.delete()
            messages.success(request, "Juego de mesa eliminado.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: el juego tiene préstamos registrados.")
        return redirect("juego_list")
    return render(
        request,
        "biblioteca/confirm_delete.html",
        {"objeto": juego, "tipo": "juego de mesa", "volver": "juego_list"},
    )


@solo_administradores
def socio_list(request):
    return render(request, "biblioteca/socio_list.html", {"socios": Socio.objects.all()})


@solo_administradores
def socio_create(request):
    form = SocioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Socio registrado correctamente.")
        return redirect("socio_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": "Nuevo socio", "volver": "socio_list"})


@solo_administradores
def socio_update(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    form = SocioForm(request.POST or None, instance=socio)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Socio actualizado correctamente.")
        return redirect("socio_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": "Editar socio", "volver": "socio_list"})


@solo_administradores
def socio_delete(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    # Prestamo.socio es CASCADE (ver justificación en el README), pero ese
    # borrado en cascada no pasa por Prestamo.eliminar_y_reponer(): si el
    # socio tuviera un préstamo sin devolver, el ejemplar quedaría
    # descontado del stock para siempre. Se bloquea ese caso en vez de
    # dejar el inventario descuadrado.
    if request.method == "POST":
        if socio.prestamos.filter(devuelto=False).exists():
            messages.error(request, "No se puede eliminar: el socio tiene préstamos sin devolver.")
        else:
            socio.delete()
            messages.success(request, "Socio eliminado.")
        return redirect("socio_list")
    return render(
        request,
        "biblioteca/confirm_delete.html",
        {"objeto": socio, "tipo": "socio", "volver": "socio_list"},
    )


@solo_administradores
def prestamo_list(request):
    empleado_id = request.GET.get("empleado", "")
    prestamos = Prestamo.objects.select_related("libro", "juego", "socio", "empleado")
    if empleado_id.isdigit():
        prestamos = prestamos.filter(empleado_id=int(empleado_id))
    context = {
        "prestamos": prestamos,
        "empleados": Empleado.objects.all(),
        "empleado_seleccionado": empleado_id,
    }
    return render(request, "biblioteca/prestamo_list.html", context)


@solo_administradores
def prestamo_create(request):
    form = PrestamoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        else:
            messages.success(request, "Préstamo registrado correctamente.")
            return redirect("prestamo_list")
    return render(request, "biblioteca/prestamo_form.html", {"form": form, "titulo": "Registrar préstamo", "volver": "prestamo_list"})


@solo_administradores
def prestamo_update(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    form = PrestamoEditForm(request.POST or None, instance=prestamo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Préstamo actualizado correctamente.")
        return redirect("prestamo_list")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": "Editar préstamo", "volver": "prestamo_list"})


@solo_administradores
def prestamo_delete(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == "POST":
        prestamo.eliminar_y_reponer()
        messages.success(request, "Préstamo eliminado.")
        return redirect("prestamo_list")
    return render(
        request,
        "biblioteca/confirm_delete.html",
        {"objeto": prestamo, "tipo": "préstamo", "volver": "prestamo_list"},
    )


@solo_administradores
def prestamo_devolver(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == "POST":
        prestamo.marcar_devuelto()
        messages.success(request, "Préstamo marcado como devuelto.")
        return redirect("prestamo_list")
    return render(request, "biblioteca/prestamo_confirm_devolucion.html", {"prestamo": prestamo, "volver": "prestamo_list"})


# --- "Mi lista de préstamos" (carrito) ---------------------------------
# Vive en la sesión (ver carrito.py), no en la base de datos. Disponible
# para cualquier socio con sesión iniciada (no solo administradores):
# permite pedir varios títulos a la vez sin pasar por el mesón. Al
# confirmar, cada línea se convierte en un Prestamo con empleado vacío.

@login_required
def carrito_agregar(request, tipo, pk):
    if tipo not in ("libro", "juego"):
        raise Http404("Tipo de producto no válido.")
    if request.method == "POST":
        carrito.agregar(request, tipo, pk)
        messages.success(request, "Se agregó a tu lista de préstamos.")
    return redirect(request.POST.get("volver", "home"))


@login_required
def carrito_ver(request):
    context = {"items": carrito.items(request), "socio": getattr(request.user, "socio", None)}
    return render(request, "biblioteca/carrito.html", context)


@login_required
def carrito_quitar(request, clave):
    carrito.quitar(request, clave)
    return redirect("carrito_ver")


@login_required
def checkout(request):
    filas = carrito.items(request)
    if not filas:
        messages.error(request, "Tu lista de préstamos está vacía.")
        return redirect("carrito_ver")
    if request.method != "POST":
        return redirect("carrito_ver")

    # El socio ya no se elige de una lista: es el que está vinculado a la
    # cuenta con sesión iniciada. Así cada quien solo puede pedir
    # préstamos para sí mismo, no a nombre de otro socio.
    socio = getattr(request.user, "socio", None)
    if not socio:
        messages.error(request, "Tu cuenta no está vinculada a un socio. Pide en el mesón que la vinculen.")
        return redirect("carrito_ver")

    generados = 0
    for fila in filas:
        if fila["producto"].stock < 1:
            messages.error(request, f"No quedan ejemplares disponibles de «{fila['producto']}».")
            continue
        datos = {"socio": socio}
        if fila["tipo"] == "libro":
            datos["libro"] = fila["producto"]
        else:
            datos["juego"] = fila["producto"]
        # Prestamo.save() hace todo el trabajo: bloquea el producto,
        # calcula la fecha de devolución y descuenta el stock (ver models.py).
        Prestamo.objects.create(**datos)
        generados += 1
        carrito.quitar(request, fila["clave"])

    if generados:
        messages.success(request, f"¡Listo! Se registraron {generados} préstamo(s).")
        return redirect("home")
    return redirect("carrito_ver")


# --- Cuenta personal: perfil, préstamos propios y foro de opiniones ----

@login_required
def perfil_editar(request):
    # get_or_create es una red de seguridad: en circunstancias normales la
    # señal de signals.py ya creó el perfil al crear la cuenta.
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tu perfil se actualizó correctamente.")
        return redirect("perfil_editar")
    return render(request, "biblioteca/form.html", {"form": form, "titulo": "Mi perfil", "volver": "home"})


@login_required
def mis_prestamos(request):
    """Solo lectura: qué tiene prestado el socio vinculado a esta cuenta y
    cuándo debe devolverlo. Marcar la devolución sigue siendo tarea del
    mesón (ver prestamo_devolver), no algo que el propio socio haga aquí."""
    socio = getattr(request.user, "socio", None)
    prestamos = []
    if socio:
        prestamos = (
            socio.prestamos.filter(devuelto=False)
            .select_related("libro", "juego")
            .order_by("fecha_devolucion_prevista")
        )
    return render(request, "biblioteca/mis_prestamos.html", {"socio": socio, "prestamos": prestamos})


@login_required
def libro_detalle(request, pk):
    libro = get_object_or_404(Libro.objects.select_related("autor"), pk=pk)
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.libro = libro
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, "Tu opinión quedó publicada.")
            return redirect("libro_detalle", pk=libro.pk)
    else:
        form = ComentarioForm()
    comentarios = libro.comentarios.select_related("usuario", "usuario__perfil")
    return render(
        request,
        "biblioteca/libro_detalle.html",
        {"libro": libro, "form": form, "comentarios": comentarios},
    )

""""Mi lista de préstamos": un carrito adaptado a una biblioteca.

Vive en la SESIÓN del navegador, no en la base de datos: es una lista
temporal de esta visita. Se guarda como un diccionario simple en
request.session, por ejemplo {"libro-3": True, "juego-1": True} (clave
"tipo-id"). Pedir prestado el mismo título dos veces no tiene sentido,
así que agregar es una operación idempotente (no se acumula cantidad).
Recién al confirmar (ver views.checkout) cada línea se convierte en una
fila permanente de Prestamo.
"""

from .models import JuegoMesa, Libro

CLAVE_SESION = "carrito"


def _datos(request):
    return request.session.setdefault(CLAVE_SESION, {})


def agregar(request, tipo, producto_id):
    carrito = _datos(request)
    carrito[f"{tipo}-{producto_id}"] = True
    request.session.modified = True


def quitar(request, clave):
    _datos(request).pop(clave, None)
    request.session.modified = True


def vaciar(request):
    request.session[CLAVE_SESION] = {}
    request.session.modified = True


def cantidad_total(request):
    return len(_datos(request))


def items(request):
    """Junto a cada clave de la lista, trae el producto real desde la BD.

    Si un libro o juego fue eliminado del catálogo mientras estaba en la
    lista de alguien, esa línea simplemente se omite.
    """
    filas = []
    for clave in list(_datos(request)):
        tipo, _, pk = clave.partition("-")
        if tipo == "libro":
            producto = Libro.objects.select_related("autor").filter(pk=pk).first()
        else:
            producto = JuegoMesa.objects.filter(pk=pk).first()
        if producto:
            filas.append({"clave": clave, "tipo": tipo, "producto": producto})
    return filas

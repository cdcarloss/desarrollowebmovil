from . import carrito


def carrito_context(request):
    """Disponible en toda plantilla como {{ carrito_cantidad }}, para
    mostrar el contador del carrito en el encabezado sin repetir la
    consulta en cada vista."""
    return {"carrito_cantidad": carrito.cantidad_total(request)}


def perfil_context(request):
    """Trae el Perfil del usuario conectado UNA vez por request, en Python
    (aquí, no en la plantilla). base.html lo usa para mostrar la foto en
    el encabezado sin disparar una consulta desde dentro del template."""
    perfil = None
    if request.user.is_authenticated:
        perfil = getattr(request.user, "perfil", None)
    return {"perfil_actual": perfil}

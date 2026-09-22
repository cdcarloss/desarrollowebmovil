from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_automatico(sender, instance, created, **kwargs):
    """Cada vez que se crea una cuenta, le genera un Perfil vacío junto
    con ella (foto y descripción quedan en blanco hasta que la persona
    las complete). Así cualquier vista puede asumir que
    request.user.perfil existe, sin tener que acordarse de crearlo a
    mano en cada lugar donde se registra un usuario."""
    if created:
        Perfil.objects.get_or_create(usuario=instance)


from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import logging

from cadastro_jogos.models import UsuarioJogos


LOGGER = logging.getLogger("django")

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def atualizar_usuario_jogos(sender, instance, **kwargs):
    '''Associa o usuário criado no sistema ao usuário que se loga via SSO'''
    try:
        if not instance.is_superuser:
            usuario_jogos = UsuarioJogos.objects.get(cpf=instance.username)
            usuario_jogos.username = instance
            usuario_jogos.save()
    except Exception:
        LOGGER.debug(f"Erro ao associar '{instance}' a modelo UsuarioJogos")

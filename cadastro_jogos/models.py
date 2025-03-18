import uuid
import logging

from django.db import models

# Create your models here.
from django.db import models
from _core.models import User

from .utils import PERFIL_CHOICES, TIPO_REGIONAL_CHOICES
from .validators import validar_cpf, validar_email
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

LOGGER = logging.getLogger("django")

class UsuarioJogos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
    )
    nome = models.CharField(
        max_length=120, 
        null=False, 
        blank=False, 
        verbose_name="Nome do usuário:",
    )
    cpf = models.CharField(
        max_length=11,
        default="",
        null=False,
        blank=False,
        unique=True,
        validators=[validar_cpf],
        verbose_name="CPF do servidor:",
    )
    email = models.CharField(
        max_length=150, 
        null=False, 
        blank=False,
        validators=[validar_email]
    )
    telefone = models.CharField(max_length=12, null=False, blank=False, verbose_name="Telefone")
    perfil = models.CharField(
        max_length=1, null=False, blank=False,
        choices=PERFIL_CHOICES
    )

    class Meta:
        verbose_name = "Usuário Jogos"
        verbose_name_plural = "Usuários Jogos"

    def __str__(self):
        return f"{self.nome} - {self.cpf}"
    

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


class Regional(models.Model):  

    nome = models.CharField(max_length=120, null=False, blank=False, verbose_name="Nome da Regional")
    numero = models.IntegerField(null=False, blank=False, verbose_name="Número")
    cidade = models.CharField(max_length=100, null=False, blank=False, verbose_name="Cidade")
    tipo_regional = models.CharField(max_length=20, choices=TIPO_REGIONAL_CHOICES, null=False, blank=False, verbose_name="Tipo de Regional")

    class Meta:
        verbose_name = "Regional"
        verbose_name_plural = "Regionais"

    def __str__(self):
        return f"{self.nome} - {self.cidade}"
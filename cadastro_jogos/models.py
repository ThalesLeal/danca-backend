from django.db import models

# Create your models here.
from django.db import models
import uuid
from _core.models import User

from .utils import PERFIL_CHOICES
from .validators import validar_cpf
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings

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
        null=True, 
        blank=True, 
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
        null=True, 
        blank=True
    )
    telefone = models.CharField(max_length=12, null=True, blank=True, verbose_name="Telefone")
    perfil = models.CharField(
        max_length=1,
        choices=PERFIL_CHOICES
    )

    class Meta:
        verbose_name = "Usuário Jogos"
        verbose_name_plural = "Usuários Jogos"

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

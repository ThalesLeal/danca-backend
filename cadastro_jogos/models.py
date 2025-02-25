from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid
from codata_sso.models import User as BaseUser
from .validators import validar_cpf
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.contrib.auth.models import Group as BaseGroup

# Create your models here.


class Usuario(models.Model):
    nome_completo = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Nome Completo"
    )
    cpf = models.CharField(
        max_length=14,
        default="",
        null=False,
        blank=False,
        unique=True,
        validators=[validar_cpf],
        verbose_name="CPF do usuário"
    )
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email")
    telefone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Telefone")
    perfil = models.CharField(
        max_length=50,
        choices=[(group.name, group.name) for group in BaseGroup.objects.all()],  # Lista os grupos existentes
        verbose_name="Perfil"
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nome_completo} - {self.cpf}"



# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def atualizar_usuario(sender, instance, **kwargs):
#     try:
#         if not instance.is_superuser:
#             # Tente encontrar o usuário cadastrado com o CPF correspondente
#             usuario, created = Usuario.objects.get_or_create(cpf=instance.username)  # Assumindo que 'username' é o CPF
#             usuario.username = instance.username  # Ensure to set the username correctly
#             usuario.save()
#             LOGGER.info(f"Usuário '{usuario}' associado ao modelo Usuario com sucesso.")
#     except Exception as e:
#         LOGGER.debug(f"Erro ao associar '{instance}' ao modelo Usuario: {e}")

# @receiver(post_delete, sender=Usuario)  
# def remover_usuario(sender, instance, **kwargs):    
#     LOGGER.info(f"Usuário '{instance}' removido do modelo Usuario.")  
#     pass  
from django.db import models
from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Model proxy para alterar a exibição no admin
class Group(BaseGroup):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")

class User(AbstractUser):
    """
    Modelo de usuário personalizado
    Login por username (nome) ao invés de CPF
    """
    foto = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

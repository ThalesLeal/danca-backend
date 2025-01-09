from django.db import models

from django.contrib.auth.models import Group as BaseGroup
from django.utils.translation import gettext_lazy as _
from codata_sso.models import User as BaseUser


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

class User(BaseUser):
    pass

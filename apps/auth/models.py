from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db import models
from django.utils.translation import gettext_lazy as _


# Model proxy para alterar a exibição no admin
class Group(BaseGroup):
    class Meta:
        proxy = True


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.get_full_name()

    def __repr__(self):
        return f"<User '{self.username}' ('{self.get_full_name()}')>"

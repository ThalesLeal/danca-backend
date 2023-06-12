from django.contrib.auth import get_user_model
from django.db import models

from _core.models import TimestampedModel

User = get_user_model()


class Exemplo(TimestampedModel):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

from django.contrib.auth import get_user_model
from django.db import models

from ..base_models import TimestampedModel


User = get_user_model()


class Example(TimestampedModel):
    name = models.CharField("nome", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Exemplo"

from django.db import models


class Example(models.Model):
    name = models.CharField("nome", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Exemplo"

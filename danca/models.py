from django.db import models


class Lote(models.Model):
    descricao = models.CharField(max_length=255)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidades = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('encerrado', 'Encerrado')], default='ativo')

    def __str__(self):
        return f"{self.descricao} - {self.status}"
    class Meta:
        ordering = ['-id']
    
class Categoria(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao
    class Meta:
        ordering = ['-id']

class TipoEvento(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao
    
    class Meta:
        ordering = ['-id']


class Evento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aberto', 'Aberto'),
        ('encerrado', 'Encerrado'),
        ('cancelado', 'Cancelado'),
    ]

    descricao = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    quantidade_pessoas = models.IntegerField(null=True, blank=True, help_text='Número máximo de vagas disponíveis')
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Valor unitário do evento')
    contador_inscricoes = models.IntegerField(default=0, editable=False, verbose_name="Inscrições")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.descricao} - {self.tipo.descricao}"

    class Meta:
        ordering = ['-data', '-id']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
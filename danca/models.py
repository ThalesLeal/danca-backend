from django.db import models
from .constants import STATUS_EVENTO, TAMANHO_CAMISA, TIPO_CAMISA, STATUS_LOTE

class Lote(models.Model):
    descricao = models.CharField(max_length=255)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidades = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_LOTE, default='ativo')

    def __str__(self):
        return f"{self.descricao} - {self.get_status_display()}"
    
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
    descricao = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    quantidade_pessoas = models.IntegerField(null=True, blank=True, help_text='Número máximo de vagas disponíveis')
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Valor unitário do evento')
    contador_inscricoes = models.IntegerField(default=0, editable=False, verbose_name="Inscrições")
    status = models.CharField(max_length=20, choices=STATUS_EVENTO, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.descricao} - {self.tipo.descricao}"
    
    class Meta:
        ordering = ['-data', '-id']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class Camisa(models.Model):
    descricao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CAMISA, default='unissex')
    quantidade = models.IntegerField(default=0)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.descricao} - {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Camisa"
        verbose_name_plural = "Camisas"
        ordering = ['tipo', '-data_atualizacao']

    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario if self.quantidade and self.valor_unitario else 0


class Planejamento(models.Model):
    descricao = models.CharField(max_length=100)   
    valor_planejado = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)    
      

    def __str__(self):
        return self.descricao    
    class Meta:
        ordering = ['-id']

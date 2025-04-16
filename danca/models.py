from django.db import models
from .constants import STATUS_EVENTO, TAMANHO_CAMISA, TIPO_CAMISA, STATUS_LOTE
from django.core.exceptions import ValidationError

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


class Artista(models.Model):
    nome = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)
    cache = models.DecimalField(max_digits=10, decimal_places=2)
    eventos = models.ManyToManyField(Evento, related_name='artistas', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'

    def save(self, *args, **kwargs):
        """
        Sobrescreves o método save para atualizar o contador de inscrições no evento.
        """
        for evento in self.eventos.all():
            if evento.quantidade_pessoas is not None:
                if evento.quantidade_pessoas <= 0:
                    raise ValidationError("Não há vagas suficientes para este evento.")
                evento.quantidade_pessoas -= 1
                evento.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Sobrescreves o método delete para atualizar o contador de inscrições no evento.
        """
        for evento in self.eventos.all():
            if evento.quantidade_pessoas is not None:
                evento.quantidade_pessoas += 1
                evento.save()
        super().delete(*args, **kwargs)


class Inscricao(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numero_parcelas = models.IntegerField(default=1)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    eventos = models.ManyToManyField(Evento, related_name='inscricao_eventos')

    def calcular_valor_total(self):
        """
        Calcula o valor total com base nos eventos associados, considerando desconto e lote.
        """
        valor_base = sum(evento.valor_unitario for evento in self.eventos.all())
        
        # Aplica o desconto
        valor_com_desconto = valor_base - self.desconto
        
        # Aplica o valor do lote
        valor_final = valor_com_desconto + self.lote.valor_unitario
        
        return valor_final

    def atualizar_valor_total(self):
        """
        Atualiza o campo valor_total após a instância ser salva e os eventos associados.
        """
        self.valor_total = self.calcular_valor_total()
        self.save(update_fields=['valor_total'])

    def save(self, *args, **kwargs):
        """
        Salva a instância sem calcular o valor total.
        """
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.categoria.descricao}"

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        ordering = ['-id']


class InscricaoEvento(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, related_name='inscricao_evento_set')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Evento da Inscrição"
        verbose_name_plural = "Eventos das Inscrições"
        unique_together = [['inscricao', 'evento']]

    def __str__(self):
        return f"{self.inscricao.nome} - {self.evento.descricao}"
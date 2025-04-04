import uuid

from django.db import models

# Create your models here.
from django.db import models
from _core.models import User

from .utils import PERFIL_CHOICES, TIPO_REGIONAL_CHOICES, REDE_DE_ENSINO_CHOICES
from .validators import validar_cpf, validar_email, validar_cpf_cnpj
from django.utils.translation import gettext_lazy as _

class UsuarioJogos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
    )
    nome = models.CharField(
        max_length=120, 
        null=False, 
        blank=False, 
        verbose_name="Nome do usuário:",
    )
    cpf = models.CharField(
        max_length=11,
        default="",
        null=False,
        blank=False,
        unique=True,
        validators=[validar_cpf],
        verbose_name="CPF do servidor:",
    )
    email = models.CharField(
        max_length=150, 
        null=True, 
        blank=True,
        validators=[validar_email]
    )
    telefone = models.CharField(max_length=12, null=False, blank=False, verbose_name="Telefone")
    perfil = models.CharField(
        max_length=1, null=False, blank=False,
        choices=PERFIL_CHOICES
    )

    class Meta:
        verbose_name = "Usuário Jogos"
        verbose_name_plural = "Usuários Jogos"

    def __str__(self):
        return f"{self.nome} - {self.cpf}"
    

class Regional(models.Model):  
    nome = models.CharField(max_length=120, null=False, blank=False, verbose_name="Nome da Regional")
    numero = models.IntegerField(null=False, blank=False, verbose_name="Número")
    cidade = models.CharField(max_length=100, null=False, blank=False, verbose_name="Cidade")
    tipo_regional = models.CharField(max_length=20, choices=TIPO_REGIONAL_CHOICES, null=False, blank=False, verbose_name="Tipo de Regional")

    class Meta:
        verbose_name = "Regional"
        verbose_name_plural = "Regionais"

    def __str__(self):
        return f"{self.nome} - {self.cidade}"  

class UsuarioRegional(models.Model):
    usuario = models.ForeignKey(UsuarioJogos, on_delete=models.CASCADE)
    data_inicio = models.DateField(null=False, blank=False, verbose_name="Data de Início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de Fim")
    regional = models.ForeignKey(Regional, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Usuário Regional"
        verbose_name_plural = "Usuários Regionais"

    def __str__(self):
        return f"{self.usuario.nome} - {self.regional.nome}"
    

class Instituicao(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False, verbose_name="Nome da Instituição")
    cep = models.CharField(max_length=10, null=False, blank=False)
    bairro = models.CharField(max_length=120, null=False, blank=False)
    logradouro = models.CharField(max_length=120, null=False, blank=False)
    numero = models.CharField(max_length=10, null=False, blank=False)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    municipio = models.CharField(max_length=60, null=False, blank=False)
    pertence_a_regional = models.BooleanField()
    tipo_regional = models.CharField(
        max_length=20, 
        choices=TIPO_REGIONAL_CHOICES, 
        null=True, 
        blank=True, 
        verbose_name="Tipo de Regional"
    )
    regional = models.ForeignKey(Regional, on_delete=models.CASCADE, null=True, blank=True)
    rede_ensino = models.CharField(
        max_length=10,
        choices=REDE_DE_ENSINO_CHOICES,
        null=True,
        blank=True,
    )
    cpf_cnpj = models.CharField(
        max_length=18, 
        null=True, 
        blank=True, 
        validators=[validar_cpf_cnpj]
    )

    def __str__(self):
        return self.nome
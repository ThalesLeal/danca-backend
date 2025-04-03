from django.test import TestCase
from django.urls import reverse
from cadastro_jogos.forms import InstituicaoForm
from cadastro_jogos.models import Instituicao
from cadastro_jogos.tests.factories import InstituicaoFactory
from django.contrib.auth import get_user_model
import factory

UserModel = get_user_model()

class InstituicaoFormTestCase(TestCase):
    def setUp(self):
        self.instituicao = InstituicaoFactory()

    def test_criar_instituicao_cpf_cnpj_valido(self):
        dados = {
            'nome': self.instituicao.nome,
            'cep': self.instituicao.cep,
            'bairro': self.instituicao.bairro,
            'logradouro': self.instituicao.logradouro,
            'numero': self.instituicao.numero,
            'complemento': self.instituicao.complemento,
            'municipio': self.instituicao.municipio,
            'pertence_a_regional': self.instituicao.pertence_a_regional,
            'tipo_regional': self.instituicao.tipo_regional,
            'regional': self.instituicao.regional,
            'rede_ensino': self.instituicao.rede_ensino,
            'cpf_cnpj': '41.296.870/0001-37',
        }
        form = InstituicaoForm(data=dados)
        self.assertTrue(form.is_valid())

    def test_criar_instituicao_cpf_cnpj_invalido(self):
        dados = {
            'nome': self.instituicao.nome,
            'cep': self.instituicao.cep,
            'bairro': self.instituicao.bairro,
            'logradouro': self.instituicao.logradouro,
            'numero': self.instituicao.numero,
            'complemento': self.instituicao.complemento,
            'municipio': self.instituicao.municipio,
            'pertence_a_regional': self.instituicao.pertence_a_regional,
            'tipo_regional': self.instituicao.tipo_regional,
            'regional': self.instituicao.regional,
            'rede_ensino': self.instituicao.rede_ensino,
            'cpf_cnpj': self.instituicao.cpf_cnpj,
        }
        form = InstituicaoForm(data=dados)
        self.assertFalse(form.is_valid())

    def test_criar_instituicao_pertence_a_regional(self):
        '''Se pertence a uma regional, o campo CPF/CNPJ não é necessário'''
        dados = {
            'nome': self.instituicao.nome,
            'cep': self.instituicao.cep,
            'bairro': self.instituicao.bairro,
            'logradouro': self.instituicao.logradouro,
            'numero': self.instituicao.numero,
            'complemento': self.instituicao.complemento,
            'municipio': self.instituicao.municipio,
            'pertence_a_regional': True,
            'tipo_regional': self.instituicao.tipo_regional,
            'regional': self.instituicao.regional,
            'rede_ensino': self.instituicao.rede_ensino,
        }
        form = InstituicaoForm(data=dados)
        self.assertTrue(form.is_valid())

    def test_criar_instituicao_nao_pertence_a_regional(self):
        '''Se não pertence a uma regional, o campo CPF/CNPJ é obrigatório'''
        dados = {
            'nome': self.instituicao.nome,
            'cep': self.instituicao.cep,
            'bairro': self.instituicao.bairro,
            'logradouro': self.instituicao.logradouro,
            'numero': self.instituicao.numero,
            'complemento': self.instituicao.complemento,
            'municipio': self.instituicao.municipio,
            'pertence_a_regional': False,
            'cpf_cnpj': '41.296.870/0001-37',
            'rede_ensino': self.instituicao.rede_ensino,
        }
        form = InstituicaoForm(data=dados)
        self.assertTrue(form.is_valid())


        
from django.test import TestCase
from django.urls import reverse
from cadastro_jogos.forms import InstituicaoForm
from cadastro_jogos.models import Instituicao
from cadastro_jogos.tests.factories import InstituicaoFactory
from django.contrib.auth import get_user_model

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

    def test_editar_instituicao(self):
        nome_atualizado = 'Nome da Instituição Atualizado'
        dados_atualizados = {
            'nome': nome_atualizado,
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
        form = InstituicaoForm(data=dados_atualizados, instance=self.instituicao)
        self.assertTrue(form.is_valid())
        instituicao_editada = form.save()
        self.assertEqual(instituicao_editada.nome, nome_atualizado)


class InstituicaoListTestCase(TestCase):
    def setUp(self):
        UserModel.objects.create_user(username='00000000000', password='000')
        self.instituicoes = InstituicaoFactory.create_batch(3)
        self.url = reverse('list_instituicoes')

    def test_redireciona_para_login_se_nao_autenticado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/oidc/login/', response.url)

    def test_lista_instituicoes_para_usuario_autenticado(self):
        self.client.login(username='00000000000', password='000')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        for instituicao in self.instituicoes:
            self.assertContains(response, instituicao.nome)


class InstituicaoDetailTestCase(TestCase):
    def setUp(self):
        UserModel.objects.create_user(username='00000000000', password='000')
        self.instituicao = InstituicaoFactory()
        self.url = reverse('detail_instituicao', kwargs={'instituicao_id': self.instituicao.id})

    def test_redireciona_para_login_se_nao_autenticado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/oidc/login/', response.url)

    def test_exibe_detalhes_para_usuario_autenticado(self):
        self.client.login(username='00000000000', password='000')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.instituicao.nome)
        self.assertContains(response, self.instituicao.municipio)


class InstituicaoDeleteTestCase(TestCase):
    def setUp(self):
        UserModel.objects.create_user(username='00000000000', password='000')
        self.instituicao = InstituicaoFactory()
        self.url = reverse('delete_instituicao', kwargs={'instituicao_id': self.instituicao.id})

    def test_redireciona_para_login_se_nao_autenticado(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/oidc/login/', response.url)

    def test_exclui_instituicao_com_usuario_autenticado(self):
        self.client.login(username='00000000000', password='000')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('list_instituicoes'))
        self.assertFalse(Instituicao.objects.filter(id=self.instituicao.id).exists())





        
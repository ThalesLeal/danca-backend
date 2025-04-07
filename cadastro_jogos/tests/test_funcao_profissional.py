import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from cadastro_jogos.models import FuncaoProfissional

User = get_user_model()

@pytest.mark.django_db
class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='00000000000',
            password='000'
        )
        self.client.login(username='00000000000', password='000')


class TestFuncaoProfissionalListView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.funcao1 = FuncaoProfissional.objects.create(
            nome='Medico',
            conselho='CRM'
        )
        self.funcao2 = FuncaoProfissional.objects.create(
            nome='Enfermeiro',
            conselho='COREN'
        )

    def test_listagem_funcoes(self):       
        resposta = self.client.get(reverse('list_funcao_profissionais'))
        assert resposta.status_code == 200
        assert len(resposta.context['object_list']) == 2
        assert 'Medico' in str(resposta.context['object_list'])
        assert 'Enfermeiro' in str(resposta.context['object_list'])

    def test_listagem_com_filtro(self):        
        resposta = self.client.get(reverse('list_funcao_profissionais') + '?q=Med')
        assert resposta.status_code == 200
        assert len(resposta.context['object_list']) == 1
        assert 'Medico' in str(resposta.context['object_list'])
        assert 'Enfermeiro' not in str(resposta.context['object_list'])

    def test_ordem_alfabetica(self):       
        resposta = self.client.get(reverse('list_funcao_profissionais'))
        assert resposta.status_code == 200
        funcoes = list(resposta.context['object_list'])
        assert funcoes[0].nome == 'Enfermeiro'
        assert funcoes[1].nome == 'Medico'

    def test_context_data(self):
        resposta = self.client.get(reverse('list_funcao_profissionais'))
        assert resposta.status_code == 200
        assert 'q' in resposta.context
        assert resposta.context['q'] == ''
        assert 'create_url' in resposta.context
        assert resposta.context['create_url'] == '/funcoes/create/'


@pytest.mark.django_db
class TestFuncaoProfissionalDetailView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.funcao = FuncaoProfissional.objects.create(
            nome="Médico",
            conselho="CRM"
        )

    def test_detail_view_status_code(self):       
        url = reverse('detail_funcao_profissional', kwargs={'funcao_id': self.funcao.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_detail_view_context(self):        
        url = reverse('detail_funcao_profissional', kwargs={'funcao_id': self.funcao.id})
        response = self.client.get(url)
        assert response.context['funcao'] == self.funcao

    def test_detail_view_404(self):        
        url = reverse('detail_funcao_profissional', kwargs={'funcao_id': 9999})
        response = self.client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestFuncaoProfissionalFormView(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.funcao = FuncaoProfissional.objects.create(
            nome="Médico",
            conselho="CRM"
        )

    def test_get_create_form(self):        
        url = reverse('create_funcao_profissional')
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'Cadastrar Função Profissional' in response.content.decode('utf-8')

    def test_get_edit_form(self):      
        url = reverse('update_funcao_profissional', kwargs={'funcao_id': self.funcao.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'Editar Função Profissional' in response.content.decode('utf-8')
        assert 'Médico' in response.content.decode('utf-8')

    def test_post_create_form(self):      
        url = reverse('create_funcao_profissional')
        data = {
            'nome': 'Enfermeiro',
            'conselho': 'COREN'
        }
        response = self.client.post(url, data)
        assert response.status_code == 302  
        assert FuncaoProfissional.objects.filter(nome='Enfermeiro').exists()

    def test_post_edit_form(self):        
        url = reverse('update_funcao_profissional', kwargs={'funcao_id': self.funcao.id})
        data = {
            'nome': 'Médico Atualizado',
            'conselho': 'CRM'
        }
        response = self.client.post(url, data)
        assert response.status_code == 302  
        self.funcao.refresh_from_db()
        assert self.funcao.nome == 'Médico Atualizado'

    def test_post_invalid_form(self):      
        url = reverse('create_funcao_profissional')
        data = {
            'nome': '',  
            'conselho': 'COREN'
        }
        response = self.client.post(url, data)
        assert response.status_code == 200  
        assert 'Este campo é obrigatório.' in response.content.decode('utf-8')

@pytest.mark.django_db
class TestFuncaoProfissionalDeleteView:
    def setup_method(self):        
        self.funcao = FuncaoProfissional.objects.create(
            nome="Médico",
            conselho="CRM"
        )
        self.delete_url = reverse('delete_funcao_profissional', kwargs={'funcao_id': self.funcao.id})

    def test_delete_funcao_profissional(self, client):       
        response = client.post(self.delete_url)
        assert response.status_code == 302  
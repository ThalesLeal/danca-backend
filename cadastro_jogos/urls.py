from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Usuario
    path('', UsuarioJogosListView.as_view(), name='list_usuarios'),
    path('usuarios/<uuid:usuario_id>/', UsuarioJogosDetailView.as_view(), name='detail_usuario'),
    path('usuarios/create/', UsuarioJogosFormView.as_view(), name='create_usuario'),
    path('usuarios/<uuid:usuario_id>/update/', UsuarioJogosFormView.as_view(), name='update_usuario'),
    path('usuarios/<uuid:usuario_id>/delete/', UsuarioJogosDeleteView.as_view(), name='delete_usuario'),

    # Regional
    path('regionais/', RegionalListView.as_view(), name='list_regionais'), 
    path('regionais/<int:regional_id>/', RegionalDetailView.as_view(), name='detail_regional'),
    path('regionais/create/', RegionalFormView.as_view(), name='create_regional'),
    path('regionais/<int:regional_id>/update/', RegionalFormView.as_view(), name='update_regional'),
    path('regionais/<int:regional_id>/delete/', RegionalDeleteView.as_view(), name='delete_regional'),
    path('get-regionais/', get_regionais, name='get_regionais'),
    
    # Usuario Regional
    path('regionais/<int:regional_id>/usuarios/', UsuarioRegionalListView.as_view(), name='list_usuario_regional'),
    path('regionais/<int:regional_id>/usuarios/<int:usuario_regional_id>/', UsuarioRegionalDetailView.as_view(), name='detail_usuario_regional'),
    path('regionais/<int:regional_id>/usuarios/create/', UsuarioRegionalFormView.as_view(), name='create_usuario_regional'),
    path('regionais/<int:regional_id>/usuarios/<int:usuario_regional_id>/update/', UsuarioRegionalFormView.as_view(), name='update_usuario_regional'),
    path('regionais/<int:regional_id>/usuarios/<int:usuario_regional_id>/delete/', UsuarioRegionalDeleteView.as_view(), name='delete_usuario_regional'),

    # Instituicao
    path('instituicoes/', InstituicaoListView.as_view(), name='list_instituicoes'),
    path('instituicoes/<int:instituicao_id>/', InstituicaoDetailView.as_view(), name='detail_instituicao'),
    path('instituicoes/create/', InstituicaoFormView.as_view(), name='create_instituicao'),
    path('instituicoes/<int:instituicao_id>/update/', InstituicaoFormView.as_view(), name='update_instituicao'),
    path('instituicoes/<int:instituicao_id>/delete/', InstituicaoDeleteView.as_view(), name='delete_instituicao'),

    # Função Profissional
    path('funcoes/', FuncaoProfissionalListView.as_view(), name='list_funcao_profissionais'),
    path('funcoes/<int:funcao_id>/', FuncaoProfissionalDetailView.as_view(), name='detail_funcao_profissional'),
    path('funcoes/create/', FuncaoProfissionalFormView.as_view(), name='create_funcao_profissional'),
    path('funcoes/<int:funcao_id>/update/', FuncaoProfissionalFormView.as_view(), name='update_funcao_profissional'),
    path('funcoes/<int:funcao_id>/delete/', FuncaoProfissionalDeleteView.as_view(), name='delete_funcao_profissional'),
    path('funcoes/get-conselho/', views.get_conselho_by_funcao, name='get_conselho_by_funcao'),    
    
]
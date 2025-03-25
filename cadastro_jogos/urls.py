from django.urls import path
from .views import *

urlpatterns = [
    path('', UsuarioJogosListView.as_view(), name='list_usuarios'),
    path('usuarios/<uuid:id>/', UsuarioJogosDetailView.as_view(), name='detail_usuario'),
    path('usuarios/create/', UsuarioJogosFormView.as_view(), name='create_usuario'),
    path('usuarios/<uuid:id>/update/', UsuarioJogosFormView.as_view(), name='update_usuario'),
    path('usuarios/<uuid:id>/delete/', UsuarioJogosDeleteView.as_view(), name='delete_usuario'),

    path('regionais/', RegionalListView.as_view(), name='list_regionais'), 
    path('regionais/<int:id>/', RegionalDetailView.as_view(), name='detail_regional'),
    path('regionais/create/', RegionalFormView.as_view(), name='create_regional'),
    path('regionais/<int:id>/update/', RegionalFormView.as_view(), name='update_regional'),
    path('regionais/<int:id>/delete/', RegionalDeleteView.as_view(), name='delete_regional'),
    
    path('regionais/<int:id>/usuarios/', UsuarioRegionalListView.as_view(), name='list_usuario_regional'),
    path('regionais/<int:id>/usuarios/<int:usuario_regional_id>/', UsuarioRegionalDetailView.as_view(), name='detail_usuario_regional'),
    path('regionais/<int:id>/usuarios/create/', UsuarioRegionalFormView.as_view(), name='create_usuario_regional'),
    path('regionais/<int:id>/usuarios/<int:usuario_regional_id>/update/', UsuarioRegionalFormView.as_view(), name='update_usuario_regional'),
    path('regionais/<int:id>/usuarios/<int:usuario_regional_id>/delete/', UsuarioRegionalDeleteView.as_view(), name='delete_usuario_regional'),
]
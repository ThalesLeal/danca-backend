from django.urls import path
from .views import *

urlpatterns = [
    path('', UsuarioJogosListView.as_view(), name='list_usuarios'),
    path('usuarios/<uuid:id>/', UsuarioJogosDetailView.as_view(), name='detail_usuario'),
    path('usuarios/create/', UsuarioJogosFormView.as_view(), name='create_usuario'),
    path('usuarios/<uuid:id>/update/', UsuarioJogosFormView.as_view(), name='update_usuario'),
    path('usuarios/<uuid:id>/delete/', UsuarioJogosDeleteView.as_view(), name='delete_usuario'),
]

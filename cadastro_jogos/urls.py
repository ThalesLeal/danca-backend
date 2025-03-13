from django.urls import path
from .views import read_usuario, update_usuario, delete_usuario, UsuarioJogosListView, UsuarioJogosFormView

urlpatterns = [
    path('', UsuarioJogosListView.as_view(), name='list_usuarios'),
    path('usuarios/create/', UsuarioJogosFormView.as_view(), name='create_usuario'),
    path('usuarios/<uuid:id>/', read_usuario, name='read_usuario'),
    path('usuarios/<uuid:id>/update/', update_usuario, name='update_usuario'),
    path('usuarios/<uuid:id>/delete/', delete_usuario, name='delete_usuario'),
]

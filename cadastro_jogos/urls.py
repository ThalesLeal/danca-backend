from django.urls import path
from .views import usuario_list, create_usuario, read_usuario, update_usuario, delete_usuario

urlpatterns = [
    path('', usuario_list, name='usuario_list'),
    path('create/', create_usuario, name='create_usuario'),
    path('usuarios/<uuid:id>/', read_usuario, name='read_usuario'),
    path('usuarios/<uuid:id>/update/', update_usuario, name='update_usuario'),
    path('usuarios/<uuid:id>/delete/', delete_usuario, name='delete_usuario'),
]

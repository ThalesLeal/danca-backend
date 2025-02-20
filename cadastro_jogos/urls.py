from django.urls import path
from .views import usuario_list, create_usuario, read_usuario, update_usuario, delete_usuario

urlpatterns = [
    path('', usuario_list, name='usuario_list'),
    path('create/', create_usuario, name='create_usuario'),
    path('<int:usuario_id>/', read_usuario, name='read_usuario'),
    path('<int:usuario_id>/update/', update_usuario, name='update_usuario'),
    path('<int:usuario_id>/delete/', delete_usuario, name='delete_usuario'),
]

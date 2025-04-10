from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #Lotes
    path('lotes/', LoteListView.as_view(), name='list_lotes'),
    path('lotes/<int:lote_id>/', LoteDetailView.as_view(), name='detail_lote'),
    path('lotes/create/', LoteFormView.as_view(), name='create_lote'),
    path('lotes/<int:lote_id>/update/', LoteFormView.as_view(), name='update_lote'),
    path('lotes/<int:lote_id>/delete/', LoteDeleteView.as_view(), name='delete_lote'),

    #Categoria
    path('categorias/', CategoriaListView.as_view(), name='list_categorias'),
    path('categorias/<int:categoria_id>/', CategoriaDetailView.as_view(), name='detail_categoria'),
    path('categorias/create/', CategoriaFormView.as_view(), name='create_categoria'),
    path('categorias/<int:categoria_id>/update/', CategoriaFormView.as_view(), name='update_categoria'),
    path('categorias/<int:categoria_id>/delete/', CategoriaDeleteView.as_view(), name='delete_categoria'),
]
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

    # Tipo de Evento
    path('tipo-eventos/', TipoEventoListView.as_view(), name='list_tipo_eventos'),
    path('tipo-eventos/<int:tipo_evento_id>/', TipoEventoDetailView.as_view(), name='detail_tipo_evento'),
    path('tipo-eventos/create/', TipoEventoFormView.as_view(), name='create_tipo_evento'),
    path('tipo-eventos/<int:tipo_evento_id>/update/', TipoEventoFormView.as_view(), name='update_tipo_evento'),
    path('tipo-eventos/<int:tipo_evento_id>/delete/', TipoEventoDeleteView.as_view(), name='delete_tipo_evento'),

    # Evento
    path('eventos/', EventoListView.as_view(), name='list_eventos'),
    path('eventos/<int:evento_id>/', EventoDetailView.as_view(), name='detail_evento'),
    path('eventos/create/', EventoFormView.as_view(), name='create_evento'),
    path('eventos/<int:evento_id>/update/', EventoFormView.as_view(), name='update_evento'),
    path('eventos/<int:evento_id>/delete/', EventoDeleteView.as_view(), name='delete_evento'),


]
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('lotes/', LoteListView.as_view(), name='list_lotes'),
    path('lotes/<int:lote_id>/', LoteDetailView.as_view(), name='detail_lote'),
    path('lotes/create/', LoteFormView.as_view(), name='create_lote'),
    path('lotes/<int:lote_id>/update/', LoteFormView.as_view(), name='update_lote'),
    path('lotes/<int:pk>/delete/', LoteDeleteView.as_view(), name='delete_lote'),
]
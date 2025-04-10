from django import template
from django.views.decorators.cache import cache_page, cache_control
from ..models import Evento

register = template.Library()

@register.filter
def format_currency(value):
    if value is None:
        return 'R$ 0,00'
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

@register.filter
@cache_page(60 * 15)  # Cache por 15 minutos
@cache_control(private=True)
def get_evento(value):
    try:
        return Evento.objects.get(id=value)
    except Evento.DoesNotExist:
        return None
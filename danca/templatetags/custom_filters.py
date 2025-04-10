from django import template

register = template.Library()

@register.filter
def format_currency(value):
    if value is None:
        return 'R$ 0,00'
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
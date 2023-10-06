from django import template


register = template.Library()


@register.simple_tag
def get_icon_message(parameter):
    opcoes = {
        "danger": "fas fa-times-circle fa-lg",
        "success": "fas fa-check-circle fa-lg",
        "info": "fas fa-info-circle fa-lg",
        "warning": "fas fa-exclamation-triangle fa-lg",
    }

    if parameter in opcoes:
        icone = opcoes[parameter]
    else:
        icone = "fas fa-info-circle fa-lg"  # Valor padrão para opções não reconhecidas

    return f"{icone}"


@register.simple_tag
def get_title_message(parameter):
    opcoes = {
        "danger": "Erro",
        "success": "Sucesso",
        "info": "Informação",
        "warning": "Atenção",
    }

    if parameter in opcoes:
        title = opcoes[parameter]
    else:
        title = "Informação"  # Valor padrão para opções não reconhecidas

    return f"{title}"

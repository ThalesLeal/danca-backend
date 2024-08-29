"""_core.context_processors.py
"""
from _conf import settings


def application(request):
    """Disponibiliza variáveis de contexto para todas os templates do projeto."""
    context = {
        "APP_ASSINATURA": settings.APP_ASSINATURA,
        "APP_ASSINATURA_URL": settings.APP_ASSINATURA_URL,
        "APP_TITULO": settings.APP_TITULO,
        "APP_TITULO_URL": settings.APP_TITULO_URL,
        "APP_SUBTITULO": settings.APP_SUBTITULO,
        "HEADER_BG_COLOR": settings.HEADER_BG_COLOR,
        "HEADER_FONT_COLOR": settings.HEADER_FONT_COLOR,
        "FOOTER_TEXT": settings.FOOTER_TEXT,
        "GOVBR_LOGO_BRANCA": settings.GOVBR_LOGO_BRANCA,
        "ALWAYS_SHOW_MENU_LATERAL": settings.ALWAYS_SHOW_MENU_LATERAL,
        "ACESSO_RAPIDO": settings.ACESSO_RAPIDO,
        "FUNCIONALIDADES": settings.FUNCIONALIDADES,
    }
    return context

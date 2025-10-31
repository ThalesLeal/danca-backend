"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView
from danca.views import (
    index, CategoriaViewSet, EventoViewSet, CamisaViewSet,
    PlanejamentoViewSet, InscricaoViewSet, ProfissionalViewSet,
    EntradaViewSet, SaidaViewSet, PagamentoViewSet, TipoEventoViewSet, LoteViewSet,
    PedidoCamisaViewSet, processar_pagamento_inscricao, processar_pagamento_pedido
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from _core.views import register, me, update_profile, change_password


admin.site.index_title = "Início"


router = DefaultRouter()
router.register(r"categorias", CategoriaViewSet, basename="categoria")
router.register(r"eventos", EventoViewSet, basename="evento")
router.register(r"camisas", CamisaViewSet, basename="camisa")
router.register(r"planejamentos", PlanejamentoViewSet, basename="planejamento")
router.register(r"inscricoes", InscricaoViewSet, basename="inscricao")
router.register(r"profissionais", ProfissionalViewSet, basename="profissional")
router.register(r"entradas", EntradaViewSet, basename="entrada")
router.register(r"saidas", SaidaViewSet, basename="saida")
router.register(r"pagamentos", PagamentoViewSet, basename="pagamento")
router.register(r"tipo-eventos", TipoEventoViewSet, basename="tipo-evento")
router.register(r"lotes", LoteViewSet, basename="lote")
router.register(r"pedidos", PedidoCamisaViewSet, basename="pedido")


urlpatterns = [
    path('', index, name='index'),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("admin/", admin.site.urls),
    path("health/", include("watchman.urls")),
    path("__debug__", include("debug_toolbar.urls")),
    path('oidc/login/', OIDCAuthenticationRequestView.as_view(), name='oidc_login'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),
    path('danca/', include('danca.urls')),
    path('api/', include(router.urls)),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', register, name='register'),
    path('api/auth/user/', me, name='user_me'),
    path('api/auth/user/profile/', update_profile, name='update_profile'),
    path('api/auth/user/change-password/', change_password, name='change_password'),
    path('api/pagamentos/processar/', processar_pagamento_inscricao, name='processar_pagamento'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

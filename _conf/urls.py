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
from django.views.generic import TemplateView
from django.shortcuts import redirect
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView


admin.site.index_title = "Início"


urlpatterns = [
    
    path("", lambda request: redirect('usuario_list'), name="index"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("admin/", admin.site.urls),
    path("health/", include("watchman.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path('cadastro_jogos/', include('cadastro_jogos.urls')),
    path('oidc/login/', OIDCAuthenticationRequestView.as_view(), name='oidc_login'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),
]


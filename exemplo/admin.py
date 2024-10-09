from reversion.admin import VersionAdmin

from django.contrib import admin

from .models import Exemplo


@admin.register(Exemplo)
class ExemploAdmin(VersionAdmin):
    list_display = ("nome", "cadastrado_em", "modificado_em")

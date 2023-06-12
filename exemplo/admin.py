from import_export.admin import ImportExportModelAdmin
from reversion.admin import VersionAdmin

from django.contrib import admin

from .models import Exemplo


@admin.register(Exemplo)
class ExemploAdmin(ImportExportModelAdmin, VersionAdmin):
    list_display = ("nome", "cadastrado_em", "modificado_em")

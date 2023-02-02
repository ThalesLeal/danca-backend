from import_export.admin import ImportExportModelAdmin
from reversion.admin import VersionAdmin

from django.contrib import admin

from .models import Example


@admin.register(Example)
class ExampleAdmin(ImportExportModelAdmin, VersionAdmin):
    list_display = ("name", "created_at", "updated_at")

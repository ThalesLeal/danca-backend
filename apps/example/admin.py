from django.contrib import admin

from .models import Example


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

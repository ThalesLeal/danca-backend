from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group as OriginalGroup
from django.utils.translation import gettext_lazy as _

from .models import User, Group

# Altera o local no menu onde os grupos são exibidos
# para ficar junto com a opção de usuários
admin.site.unregister(OriginalGroup)
admin.site.register(Group, GroupAdmin)


class UserAdmin(BaseUserAdmin):
    add_form_template = None

    fieldsets = (
        (
            _("Personal info"),
            {"fields": ("username", "first_name", "last_name", "email")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ("username", "first_name", "last_name", "email", "last_login", "date_joined")

    def get_form(self, *args, **kwargs):
        # Remove help text do username, já que não é cadastrado/editado
        help_texts = {"username": None}
        kwargs |= {"help_texts": help_texts}
        return super().get_form(*args, **kwargs)


admin.site.register(User, UserAdmin)

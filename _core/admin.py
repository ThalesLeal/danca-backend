from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group as OriginalGroup

from codata_sso.admin import UserAdmin as BaseUserAdmin

from .models import User, Group

# Altera o local no menu onde os grupos são exibidos
# para ficar junto com a opção de usuários
admin.site.unregister(OriginalGroup)
admin.site.register(Group, GroupAdmin)

admin.site.register(User, BaseUserAdmin)

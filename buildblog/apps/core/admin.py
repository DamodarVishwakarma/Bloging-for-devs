from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as StockGroup
from django.utils.translation import gettext_lazy as _

from core.forms import UserChangeForm, UserCreationForm
from core.models import CUser, Group
from core.settings import CUSER_SETTINGS

@admin.register(CUser)
class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/core/core/add_form.html'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_agent', 'is_manager')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2' ),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_active', 'is_staff', 'is_agent', 'is_manager')
    search_fields = ('email',)
    ordering = ('email',)

if CUSER_SETTINGS['register_proxy_auth_group_model']:
    admin.site.unregister(StockGroup)

    @admin.register(Group)
    class GroupAdmin(BaseGroupAdmin):
        pass

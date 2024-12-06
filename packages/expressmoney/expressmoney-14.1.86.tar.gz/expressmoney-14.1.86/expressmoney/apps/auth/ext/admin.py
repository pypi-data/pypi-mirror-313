from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, User
from django.db.models import ForeignKey, OneToOneField
from rest_framework.authtoken.models import TokenProxy

from . import models


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'name', 'comment')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Group)
class GroupAdmin(GroupAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('=id', '=username')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    readonly_fields = ('is_active', 'is_superuser', 'password', 'user_permissions', 'date_joined', 'last_login',
                       'last_name',
                       )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Ext)
class ExtAdmin(admin.ModelAdmin):
    list_display = ('created', 'updated', 'user', 'phonenumber', 'department', 'ip', 'http_referer')
    search_fields = ('=user__id', '=phonenumber')
    ordering = ('-created', )
    formfield_overrides = {
        ForeignKey: {'widget': AdminTextInputWidget},
        OneToOneField: {'widget': AdminTextInputWidget},
    }

    def has_delete_permission(self, request, obj=None):
        return False

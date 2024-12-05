from django.contrib import admin

from . import models


@admin.register(models.BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user_id', 'is_active', 'bin', 'number', 'expiry_month', 'expiry_year')
    list_filter = ('created',)
    search_fields = ('=id', '=user_id',)
    readonly_fields = ('user_id', 'bin', 'number', 'expiry_month', 'expiry_year', 'token')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib import admin
from django.db.models import Q

from . import models


class IsApprovedFilter(admin.SimpleListFilter):
    title = 'Одобренные заявки'
    parameter_name = "is_approved"

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(amount_approved__gt=0)
        if self.value() == "no":
            return queryset.filter(~Q(amount_approved__gt=0))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user_id', 'is_first_loan', 'is_first_order',
                    'amount_requested', 'amount_approved', 'amount_approved_max',
                    'attempts', 'promocode_code', 'status')
    list_filter = ('created', IsApprovedFilter, 'status', 'is_first_loan', 'is_first_order')
    search_fields = ('=id', '=user_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

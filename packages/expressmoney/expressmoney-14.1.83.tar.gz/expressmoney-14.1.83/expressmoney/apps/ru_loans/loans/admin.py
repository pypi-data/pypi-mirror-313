from django.contrib import admin

from . import models


class ProlongateFilter(admin.SimpleListFilter):
    title = 'Пролонгированный займ'
    parameter_name = "is_prolongate"

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(status='OPEN', extended_end_date__isnull=False)
        else:
            return queryset


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'status', 'order', 'user_id', 'expiry_date', 'closed_date',
                    'interest_rate', 'period', 'free_period',
                    'body_issue', 'body_paid', 'body_balance',
                    'interests_charged', 'interests_paid', 'interests_balance',
                    'balance',
                    )
    list_filter = ('status', 'created', ProlongateFilter)
    search_fields = ('=id', '=order__id', '=order__user_id')

    @staticmethod
    def user_id(obj):
        return obj.order.user_id

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

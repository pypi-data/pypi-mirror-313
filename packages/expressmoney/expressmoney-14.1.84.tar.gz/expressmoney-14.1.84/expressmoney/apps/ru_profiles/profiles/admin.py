from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_id', 'last_name', 'first_name', 'middle_name', 'birth_date',
                    'identified', 'verified',
                    'passport_serial', 'passport_number', 'snils'
                    )
    search_fields = ('=user_id', '=passport_number', '=snils', '=last_name', '=first_name', '=middle_name')
    list_filter = ('created', 'identified', 'verified')
    ordering = ('-created',)
    readonly_fields = ('user_id',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

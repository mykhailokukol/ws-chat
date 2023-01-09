from django.contrib import admin

from authapp import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'email',
        'username',
        'is_superuser',
        'is_active',
        'is_staff',
    )
    read_only_fields = (
        'id',
        'is_online',
        'date_created',
        'date_updated',
    )
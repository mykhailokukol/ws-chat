from django.contrib import admin

from authapp import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'id',
        'email',
        'username',
        'is_superuser',
        'is_active',
        'is_staff',
        'is_online',
        'date_created',
        'date_updated',
    )
    read_only_fields = (
        'id',
        'is_online',
        'date_created',
        'date_updated',
    )
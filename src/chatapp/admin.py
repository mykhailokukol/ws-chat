from django.contrib import admin

from chatapp import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    fields = (
        'author',
        'room',
        'text',
        'is_read',
        'is_changed',
    )
    read_only_fields = ('id', 'date_created')


class MessageInline(admin.TabularInline):
    model = models.Message
    fk_name = 'room'
    extra = 0


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline
    ]
    fields = (
        'name',
    )
    read_only_field = ('id', )

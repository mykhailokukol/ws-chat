from django.contrib import admin

from chatapp import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    fields = (
        'id',
        'author',
        'room',
        'text',
        'date_created',
        'is_read',
        'is_changed',
    )
    read_only_fields = ('id', 'date_created')
    

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    field = (
        'id',
        'name',
    )
    read_only_field = ('id', )

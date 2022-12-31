from django.urls import path

from channels.routing import URLRouter

from chatapp import consumers


wsurlpatterns = URLRouter([
    path('api/ws/chat/', consumers.ChatRoomConsumer.as_asgi()),
])
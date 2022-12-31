from django.urls import path, re_path

from channels.routing import URLRouter

from chatapp import consumers


wsurlpatterns = URLRouter([
    re_path(r'api/ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
])
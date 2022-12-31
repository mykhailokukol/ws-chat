import json
from termcolor import cprint

from asgiref.sync import async_to_sync

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.db import IntegrityError

from chatapp.models import Room, Message


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """  """
    
    async def connect(self):
        
        room = await self.get_room(self.scope['url_route']['kwargs']['room_name'])
        if not room:
            return await self.close()
        
        self.room = room
        self.room_group_name = f'chat_{room.name}'
        
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        await self.accept()
        
    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        
        username = text_data['username']
        message = text_data['message']
        
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )
        
    async def disconnect(self, code):
        return await super().disconnect(code)
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'message': message, 
            'username': username,
        }))
    
    @database_sync_to_async
    def get_room(self, name):
        room_exists = Room.objects.filter(name=name).exists()
        if room_exists:
            return Room.objects.filter(name=name).last()
        else:
            try:
                return Room.objects.create(name=name)
            except IntegrityError:
                return None
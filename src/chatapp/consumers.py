import json, jwt
from datetime import datetime
from termcolor import cprint
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.db import IntegrityError
from django.conf import settings

from authapp.serializers import UserSerializer
from chatapp.serializers import MessageSerializer
from chatapp.models import Room, Message
from authapp.models import User


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """  """
    
    def get_query_parameter(self, name: str):
        try:
            return self.params[name][-1]
        except KeyError:
            cprint('Invalid parameter or no parameter was given.', 'red')
    
    async def connect(self):
        self.params = parse_qs(self.scope['query_string'].decode('utf-8'), encoding='utf-8')
        
        user = self.get_query_parameter('token')
        self.user = await self.get_user_by_token(user)
        
        await self.accept()
        
        if not self.user:
            return await self.close()
        
        self.room = await self.get_room(self.scope['url_route']['kwargs']['room_name'])
        if not self.room:
            return await self.close()
        
        self.room_group_name = f'chat_{self.room.name}'
        
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        old_messages = await self.get_old_messages(self.room)
        for message in old_messages:
            await self.channel_layer.group_send(
                    self.room_group_name, {
                        'type': 'old_messages',
                        'message': message
                    }
                )
        
    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        
        if 'message' in text_data:
            message = text_data['message']
            
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                }
            )
            await self.save_message(message, self.user, self.room)
        if 'read_messages' in text_data:
            await self.read_messages(text_data['read_messages'], self.room)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'system_info',
                    'text': f'Messages read by {self.user}.'
                }
            )
            
    async def disconnect(self, code):
        return await super().disconnect(code)
    
    async def system_info(self, event: dict):
        text = event['text']
        await self.send(text_data=json.dumps({
            'system_info': text,
        }))
    
    async def chat_message(self, event: dict):
        message = event['message']
        user = await self.get_user_by_username(event['username'])
        
        await self.send(text_data=json.dumps({
            'message': message, 
            'user': user,
        }))
        
    async def old_messages(self, event: dict):
        message = event['message']
        
        await self.send(text_data=json.dumps(message))
    
    @database_sync_to_async
    def get_old_messages(self, room: Room = None):
        if not room:
            room = self.room
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return serializer.data
    
    @database_sync_to_async
    def read_messages(self, messages: list, room: Room = None):
        if not room:
            room = self.room
        if messages == 'all':
            messages = Message.objects.filter(room=room, is_read=False).exclude(author=self.user)
        else:
            messages = Message.objects.filter(id__in=messages, room=room, is_read=False).exclude(author=self.user)
        for message in messages:
            message.is_read = True
            message.save()
    
    @database_sync_to_async
    def get_user_by_token(self, token: str):
        try:
            decoded_user_token = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM']
            )
            user_id = int(decoded_user_token['user_id'])
            user = User.objects.filter(id=user_id)
            if user.exists():
                return user.last()
            return None
        except jwt.exceptions.DecodeError as e:
            cprint(e, 'red')
            return None
        
    @database_sync_to_async
    def get_user_by_username(self, username: str):
        user = User.objects.filter(username=username)
        if user.exists():
            data = UserSerializer(user.last()).data
            return data
        return None
    
    @database_sync_to_async
    def get_room(self, name: str):
        room_exists = Room.objects.filter(name=name).exists()
        if room_exists:
            return Room.objects.filter(name=name).last()
        else:
            try:
                return Room.objects.create(name=name)
            except IntegrityError:
                return None
    
    @database_sync_to_async
    def save_message(self, text: str, author: User, room: Room):
        return Message.objects.create(
            text=text,
            author=author,
            room=room,
        )
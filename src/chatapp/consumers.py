from termcolor import cprint

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """  """
    
    async def connect(self):
        cprint('Connected', 'green')
        await self.accept()
        
    async def receive(self, text_data=None, bytes_data=None):
        cprint(f'Received: {text_data}', 'yellow')
        await self.send(text_data)
        
    async def disconnect(self, code):
        cprint('Disconnected', 'red')
        return await super().disconnect(code)
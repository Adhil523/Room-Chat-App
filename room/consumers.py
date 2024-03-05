import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room,Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name='chat_%s' % self.room_name
        print(self.room_group_name)
        await self.channel_layer.group_add(        #to create a group name
            self.room_group_name,
            self.channel_name
        )
        print("Reached connect")
        await self.accept()
        await self.send(text_data=json.dumps({         #the message is being sent to the html page to the backend
            'type':'connection_estbaished',
            'message':'You are now connected'
        }))
    
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self,text_data):
        data=json.loads(text_data)
        print(data)
        message=data['message']
        username=data['username']
        room=data['room']

        await self.save_message(username,room,message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room
            }
        )
    async def chat_message(self,event):
        print("Reached chat-message")
        message=event['message']
        username=event['username']
        room=event['room']
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'room':room
        }))
    
    @sync_to_async
    def save_message(self,username,room,message):
        user=User.objects.get(username=username)
        room=Room.objects.get(slug=room)
        Message.objects.create(user=user,room=room,content=message)
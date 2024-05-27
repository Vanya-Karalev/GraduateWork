import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from movies.models import *
from users.models import *
from django.shortcuts import get_object_or_404


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'pause_state' in text_data_json:
            room_name = text_data_json['room_name']
            new_pause_state = text_data_json['pause_state']
            await self.update_pause_state(room_name, new_pause_state)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'pause_state',
                    'pause_state': new_pause_state,
                }
            )
        elif 'timer_state' in text_data_json:
            room_name = text_data_json['room_name']
            new_timer_state = text_data_json['timer_state']
            await self.update_timer_state(room_name, new_timer_state)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'timer_state',
                    'timer_state': new_timer_state,
                }
            )
        else:
            message = text_data_json
            event = {
                'type': 'send_message',
                'message': message,
            }
            await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    async def pause_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'pause_state',
            'pause_state': event['pause_state']
        }))

    async def timer_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'timer_state',
            'timer_state': event['timer_state']
        }))

    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        if not Message.objects.filter(message=data['message']).exists():
            user = get_object_or_404(CustomUser, username=data['sender'])
            new_message = Message(room=get_room_by_name, sender=user, message=data['message'])
            new_message.save()

    @database_sync_to_async
    def update_pause_state(self, room_name, new_pause_state):
        room = Room.objects.get(room_name=room_name)
        room.pause = new_pause_state
        room.save()

    @database_sync_to_async
    def update_timer_state(self, room_name, new_timer_state):
        room = Room.objects.get(room_name=room_name)
        room.timer = new_timer_state
        room.save()

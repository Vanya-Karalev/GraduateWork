import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from movies.models import *
from users.models import *
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        # url_room = self.room_name.replace("room_", "")
        # room = get_object_or_404(Room, room_name=url_room)
        # room.delete()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(text_data_json)
        elif message_type == 'video_event':
            await self.handle_video_event(text_data_json)

    async def handle_chat_message(self, data):
        event = {
            'type': 'send_chat_message',
            'message': data,
        }
        await self.channel_layer.group_send(self.room_name, event)

    async def handle_video_event(self, data):
        event = {
            'type': 'send_video_event',
            'event': data,
        }
        await self.channel_layer.group_send(self.room_name, event)

        if not data.get('user_action', False):
            # Если событие вызвано программно (не пользователем),
            # выполните необходимые действия, например, сохранение времени видео в базе данных
            await self.save_video_time(data)

    @database_sync_to_async
    def save_video_time(self, data):
        room = Room.objects.get(room_name=data['room_name'])
        room.timer = data['time']
        room.save()

    async def send_chat_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'type': 'chat_message',
            'message': {
                'sender': data['sender'],
                'message': data['message']
            }
        }
        await self.send(text_data=json.dumps(response_data))

    async def send_video_event(self, event):
        data = event['event']
        response_data = {
            'type': 'video_event',
            'event': {
                'action': data['action'],
                'time': data['time'],
            }
        }
        await self.send(text_data=json.dumps(response_data))

    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        if not Message.objects.filter(message=data['message']).exists():
            user = get_object_or_404(CustomUser, username=data['sender'])
            new_message = Message(room=get_room_by_name, sender=user, message=data['message'])
            new_message.save()
